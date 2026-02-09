import os
import sys
import numpy as np
import pandas as pd
import time
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import load_model

# Configurare Căi
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'trained_model.h5')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler_spdt.gz')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'generated', 'dataset_final.csv')

print("=== NIVEL 3 BONUS: ANALIZĂ & COMPARARE ===")

# Încărcare Date
df = pd.read_csv(DATA_PATH)
X = df.drop('Clasa', axis=1).values
y = df['Clasa'].values
scaler = joblib.load(SCALER_PATH)
X_scaled = scaler.transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# 1. MLP Benchmark
mlp_model = load_model(MODEL_PATH)
start = time.time()
y_pred_mlp = np.argmax(mlp_model.predict(X_test, verbose=0), axis=1)
t_mlp = (time.time() - start) / len(X_test) * 1000
acc_mlp = accuracy_score(y_test, y_pred_mlp)

# 2. Random Forest Benchmark
rf = RandomForestClassifier(n_estimators=100, max_depth=10)
rf.fit(X_train, y_train)
start = time.time()
y_pred_rf = rf.predict(X_test)
t_rf = (time.time() - start) / len(X_test) * 1000
acc_rf = accuracy_score(y_test, y_pred_rf)

print(f"\n[REZULTATE COMPARATIVE]")
print(f"MLP (Rețea):     Acc={acc_mlp:.4f} | Latență={t_mlp:.3f} ms")
print(f"Random Forest:   Acc={acc_rf:.4f} | Latență={t_rf:.3f} ms")

# 3. Analiză Erori
errors = np.where(y_pred_mlp != y_test)[0]
print(f"\n[ANALIZĂ ERORI] Total greșeli: {len(errors)}")
clase = ['Mare', 'Medie', 'Mica']
for i in errors[:5]:
    real_val = scaler.inverse_transform([X_test[i]])[0]
    # Calcul eroare poziție fizică
    err_pos = np.sqrt((real_val[0]-real_val[2])**2 + (real_val[1]-real_val[3])**2)
    print(f"- Real: {clase[y_test[i]]} vs Pred: {clase[y_pred_mlp[i]]} (Err Poz: {err_pos:.2f} mm)")