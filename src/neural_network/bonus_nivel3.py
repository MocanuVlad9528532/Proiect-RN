import numpy as np
import pandas as pd
import time
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from tensorflow.keras.models import load_model
import os

# CONFIGURARE
FISIER_MODEL_KERAS = 'models/trained_model.h5'
FISIER_SCALER = 'models/scaler_spdt.gz'
FISIER_DATE = 'baza_de_date_robot.csv'

print("=== NIVEL 3 BONUS (LITE): ENGINE START ===")

# 1. PREGĂTIRE DATE
df = pd.read_csv(FISIER_DATE)
X = df[['PI_X','PI_Y','PR_X','PR_Y','VI','VR','AI','AR']].values
y = df['Clasa'].values 

scaler = joblib.load(FISIER_SCALER)
X_scaled = scaler.transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# ==============================================================================
# ACTIVITATEA 1: COMPARARE ARHITECTURI (MLP vs Random Forest)
# ==============================================================================
print("\n[1] COMPARARE ARHITECTURI...")

# A. Modelul MLP (Existent)
mlp_model = load_model(FISIER_MODEL_KERAS)
start_mlp = time.time()
y_pred_mlp = np.argmax(mlp_model.predict(X_test, verbose=0), axis=1)
time_mlp = (time.time() - start_mlp) / len(X_test) * 1000 
acc_mlp = accuracy_score(y_test, y_pred_mlp)
print(f"-> MLP (Neural Net): Acc={acc_mlp:.4f}, Latency={time_mlp:.3f} ms/sample")

# B. Modelul Random Forest (Alternativa Clasică)
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)
start_rf = time.time()
y_pred_rf = rf_model.predict(X_test)
time_rf = (time.time() - start_rf) / len(X_test) * 1000 
acc_rf = accuracy_score(y_test, y_pred_rf)
print(f"-> Random Forest:    Acc={acc_rf:.4f}, Latency={time_rf:.3f} ms/sample")

# ==============================================================================
# ACTIVITATEA 3: ANALIZĂ 5 EXEMPLE GREȘITE (Confusion Analysis)
# ==============================================================================
print("\n[3] ANALIZĂ ERORI (Exemple Greșite)...")

wrong_indices = np.where(y_pred_mlp != y_test)[0]

if len(wrong_indices) == 0:
    print("Model perfect (0 erori pe test set)!")
else:
    print(f"S-au găsit {len(wrong_indices)} erori. Afișăm primele 5:")
    clase = ['Mare', 'Medie', 'Mica']
    
    for i, idx in enumerate(wrong_indices[:5]):
        sample = X_test[idx]
        true_lbl = y_test[idx]
        pred_lbl = y_pred_mlp[idx]
        
        # Recuperare valori originale
        original = scaler.inverse_transform([sample])[0]
        # Calculăm eroarea de poziție fizică
        err_fizica = np.sqrt((original[0]-original[2])**2 + (original[1]-original[3])**2)
        
        print(f"\n--- Eroare #{i+1} ---")
        print(f"Eroare Pozitie: {err_fizica:.2f} mm")
        print(f"Real: {clase[true_lbl]} | Prez: {clase[pred_lbl]}")