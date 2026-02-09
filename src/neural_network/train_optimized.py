import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# --- CONFIGURARE CĂI ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(BASE_DIR)

from src.preprocessing.combine_datasets import genereaza_set_date, augmenteaza_prin_jitter

DIRS = {
    'models': os.path.join(BASE_DIR, 'models'),
    'results': os.path.join(BASE_DIR, 'results'),
    'docs': os.path.join(BASE_DIR, 'docs')
}
for d in DIRS.values():
    if not os.path.exists(d): os.makedirs(d)

FILES = {
    'model': os.path.join(DIRS['models'], 'trained_model.h5'),
    'scaler': os.path.join(DIRS['models'], 'scaler_spdt.gz'),
    'tuning_log': os.path.join(DIRS['results'], 'hyperparameter_log.csv'),
    'tuning_plot': os.path.join(DIRS['docs'], 'hyperparameter_tuning.png')
}

print("=== ETAPA 5: ANTRENARE OPTIMIZATĂ (GRID SEARCH) ===")
np.random.seed(42); tf.random.set_seed(42)

# 1. GENERARE & PREPROCESARE
X, Y_simplu = genereaza_set_date(6000)

# Split Stratificat
X_train, X_temp, y_train, y_temp = train_test_split(X, Y_simplu, test_size=0.30, random_state=42, stratify=Y_simplu)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)

# Scalare
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
joblib.dump(scaler, FILES['scaler'])

# --- MODIFICARE CRITICĂ AICI ---
# Convertim la One-Hot Encoding ÎNAINTE de augmentare
y_train_onehot = to_categorical(y_train, num_classes=3)
y_val_onehot = to_categorical(y_val, num_classes=3)

# Acum augmentarea va funcționa corect cu matrici
X_train_final, y_train_final = augmenteaza_prin_jitter(X_train_scaled, y_train_onehot)
# -------------------------------

# 2. DEFINIRE GRID SEARCH
param_grid = {
    'neurons': [32, 64],       # Testăm 2 dimensiuni de rețea
    'learning_rate': [0.001, 0.0001], # Testăm 2 viteze de învățare
    'batch_size': [32, 64]     # Testăm 2 mărimi de lot
}

best_acc = 0.0
best_params = {}
best_model = None
results = []

total_combinations = len(param_grid['neurons']) * len(param_grid['learning_rate']) * len(param_grid['batch_size'])
current_run = 0

print(f"--> Start optimizare pe {total_combinations} combinații...")

for neurons in param_grid['neurons']:
    for lr in param_grid['learning_rate']:
        for batch in param_grid['batch_size']:
            current_run += 1
            print(f"\n[RUN {current_run}/{total_combinations}] Testing: Neurons={neurons}, LR={lr}, Batch={batch}")
            
            # Construire model dinamic
            model = Sequential([
                Dense(neurons, input_dim=8, activation='relu'),
                Dropout(0.2), # Dropout pentru regularizare
                Dense(neurons // 2, activation='relu'),
                Dense(3, activation='softmax')
            ])
            
            model.compile(
                loss='categorical_crossentropy',
                optimizer=Adam(learning_rate=lr),
                metrics=['accuracy']
            )
            
            # Antrenare scurtă (Early Stopping agresiv pentru viteză)
            early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
            
            history = model.fit(
                X_train_final, y_train_final, # Folosim datele gata procesate
                validation_data=(X_val_scaled, y_val_onehot),
                epochs=30, # Maxim 30 epoci per test
                batch_size=batch,
                callbacks=[early_stop],
                verbose=0 # Fără spam în consolă
            )
            
            # Evaluare
            val_loss, val_acc = model.evaluate(X_val_scaled, y_val_onehot, verbose=0)
            print(f"   -> Result: Val_Acc = {val_acc:.4f}")
            
            results.append({
                'neurons': neurons,
                'lr': lr,
                'batch': batch,
                'accuracy': val_acc
            })
            
            # Salvare cel mai bun model
            if val_acc > best_acc:
                best_acc = val_acc
                best_params = {'neurons': neurons, 'lr': lr, 'batch': batch}
                best_model = model
                print("   -> NEW BEST MODEL FOUND!")

# 3. SALVARE REZULTATE FINALE
print(f"\n=== FINAL OPTIMIZATION RESULT ===")
print(f"Best Accuracy: {best_acc:.4f}")
print(f"Best Params: {best_params}")

# Salvare log
pd.DataFrame(results).to_csv(FILES['tuning_log'], index=False)

# Salvare model câștigător
if best_model:
    best_model.save(FILES['model'])
    print(f"[OK] Cel mai bun model a fost salvat în: {FILES['model']}")

# Generare Grafic Comparativ
try:
    df_res = pd.DataFrame(results)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_res, x='neurons', y='accuracy', hue='lr')
    plt.title(f"Optimizare Hiperparametri (Best: {best_acc:.2%})")
    plt.ylim(0.8, 1.0) # Focus pe zona de sus
    plt.ylabel("Acuratețe Validare")
    plt.savefig(FILES['tuning_plot'])
    print(f"[OK] Grafic salvat în: {FILES['tuning_plot']}")
except Exception as e:
    print(f"[Warn] Eroare la plotare: {e}")