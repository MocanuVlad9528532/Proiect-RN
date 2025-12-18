import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, f1_score, accuracy_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import joblib 
import os

# ==========================================
# 1. CONFIGURARE PROIECT
# ==========================================
print("=== INITIALIZARE PROIECT SPDT (ETAPA 5) ===")

NUMAR_ESANTIOANE = 6000   
DIMENSIUNE_INPUT = 8      
DIMENSIUNE_OUTPUT = 3     

# Definim structura de foldere
FOLDERS = ['models', 'results', 'docs']
for folder in FOLDERS:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"[OK] Creat folder: {folder}/")

FISIER_MODEL = 'models/trained_model.h5'
FISIER_SCALER = 'models/scaler_spdt.gz'
FISIER_DATE = 'baza_de_date_robot.csv'
FISIER_ISTORIC = 'results/training_history.csv'
FISIER_GRAFIC = 'docs/loss_curve.png'

# Setăm seed pentru reproductibilitate
np.random.seed(42)
tf.random.set_seed(42)

# ==========================================
# 2. GENERARE DATE (Simulare Cinematică)
# ==========================================
def genereaza_set_date(n_samples):
    print("-> Generare date simulate...")
    P_IX = np.random.uniform(0, 1000, n_samples)
    P_IY = np.random.uniform(0, 1000, n_samples)
    V_I = np.abs(np.sin(P_IX / 200.0)) * 100.0 
    A_I = np.abs(np.cos(V_I / 20.0)) * 50.0

    X_data = []
    Y_labels = [] 
    segment = n_samples // 3

    # Generăm cele 3 clase cu zgomot specific
    for i in range(n_samples):
        # Determinam clasa in functie de index
        if i < segment: cls = 0; noise_lvl = 0.5   # Clasa Mare (OK)
        elif i < segment*2: cls = 1; noise_lvl = 12.0 # Clasa Medie (Warn)
        else: cls = 2; noise_lvl = 60.0 # Clasa Mica (Critical)

        # Injectam zgomotul de proces (Defectul fizic)
        row = [
            P_IX[i], P_IY[i], 
            P_IX[i] + np.random.normal(cls*10, noise_lvl), # Pozitie Reala X
            P_IY[i] + np.random.normal(cls*10, noise_lvl), # Pozitie Reala Y
            V_I[i], 
            V_I[i] + np.random.normal(cls*2, noise_lvl/3), # Viteza Reala
            A_I[i], 
            A_I[i] + np.random.normal(cls*1, noise_lvl/5)  # Accelerație Reala
        ]
        X_data.append(row)
        Y_labels.append(cls)

    return np.array(X_data), np.array(Y_labels)

# ==========================================
# 3. AUGMENTARE DATE (Jittering)
# ==========================================
def augmenteaza_prin_jitter(X, y, noise_scale=0.01):
    """ Adaugă zgomot fin pentru a simula vibrații senzori """
    print(f"-> AUGMENTARE: Aplicare Jitter pe {len(X)} exemple...")
    noise = np.random.normal(0, noise_scale, X.shape)
    X_aug = X + noise
    # Dublăm setul de date
    X_final = np.concatenate((X, X_aug), axis=0)
    y_final = np.concatenate((y, y), axis=0)
    return X_final, y_final

# ==========================================
# 4. PREPROCESARE & SPLIT
# ==========================================
X, Y_simplu = genereaza_set_date(NUMAR_ESANTIOANE)

# Salvare CSV Date Brute (pentru referință)
df = pd.DataFrame(X, columns=['PI_X','PI_Y','PR_X','PR_Y','VI','VR','AI','AR'])
df['Clasa'] = Y_simplu
df.to_csv(FISIER_DATE, index=False)

Y = to_categorical(Y_simplu, num_classes=3)

# --- SPLIT STRATIFICAT 70% / 15% / 15% ---
# Pas 1: 70% Train, 30% Temp
X_train, X_temp, y_train, y_temp = train_test_split(X, Y, test_size=0.30, random_state=42, stratify=Y)
# Pas 2: 15% Val, 15% Test
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)

print(f"-> Split Final: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")

# Normalizare (Scaling)
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Salvare Scaler (Critic pentru UI)
joblib.dump(scaler, FISIER_SCALER)
print(f"[OK] Scaler salvat: {FISIER_SCALER}")

# Aplicare Augmentare (Doar pe Train!)
X_train_final, y_train_final = augmenteaza_prin_jitter(X_train_scaled, y_train)

# ==========================================
# 5. ANTRENARE MODEL (Nivel 1 & 2)
# ==========================================
model = Sequential([
    Dense(32, input_dim=DIMENSIUNE_INPUT, activation='relu'),
    Dense(16, activation='relu'),
    Dense(DIMENSIUNE_OUTPUT, activation='softmax')
])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001, verbose=1)

print("\n=== START ANTRENARE ===")
history = model.fit(
    X_train_final, y_train_final, 
    epochs=50,              # Limita maximă (se va opri mai devreme)
    batch_size=32, 
    validation_data=(X_val_scaled, y_val),
    callbacks=[early_stopping, lr_scheduler], 
    verbose=1
)

# ==========================================
# 6. SALVARE REZULTATE (CSV & Grafice)
# ==========================================
# A. Salvare Istoric în CSV
df_history = pd.DataFrame(history.history)
df_history.index.name = 'Epoch'
df_history.to_csv(FISIER_ISTORIC)
print(f"[OK] Istoric antrenare exportat în: {FISIER_ISTORIC}")

# B. Salvare Grafic Loss
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Curba de Învățare (Loss)')
plt.xlabel('Epoci')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.savefig(FISIER_GRAFIC)
print(f"[OK] Grafic Loss salvat în: {FISIER_GRAFIC}")

# ==========================================
# 7. EVALUARE FINALĂ
# ==========================================
print("\n=== RAPORT FINAL PE TEST SET ===")
y_pred_prob = model.predict(X_test_scaled)
y_pred_class = np.argmax(y_pred_prob, axis=1)
y_true_class = np.argmax(y_test, axis=1)

acc = accuracy_score(y_true_class, y_pred_class)
f1 = f1_score(y_true_class, y_pred_class, average='macro')

print(f"-> Acuratețe: {acc*100:.2f}% (Target >= 75%)")
print(f"-> F1-Score:  {f1:.4f}      (Target >= 0.70)")

if acc >= 0.75 and f1 >= 0.70:
    print(">>> SUCCESS: Criteriile de Nivel 2 au fost atinse! <<<")
else:
    print(">>> ATENTIE: Verificați parametrii.")

# Salvare Model
model.save(FISIER_MODEL)
print(f"[OK] Model final salvat în: {FISIER_MODEL}")
print("=== PROCES COMPLET ===")