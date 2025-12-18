import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import joblib
import os

# ==========================================
# CONFIGURARE (Incarcare din folder models)
# ==========================================
FISIER_MODEL = 'models/trained_model.h5'
FISIER_SCALER = 'models/scaler_spdt.gz'

if not os.path.exists(FISIER_MODEL):
    print("EROARE: Nu găsesc 'models/trained_model.h5'. Rulează antrenarea întâi!")
    exit()

print("Încărcare model antrenat și scaler...")
model = load_model(FISIER_MODEL)
scaler = joblib.load(FISIER_SCALER)

# ==========================================
# DEMO UI - INFERENȚĂ REALĂ
# ==========================================
np.random.seed(None) # Random real
print("\n--- UI DEMO: DIAGNOZĂ LIVE ---")

# Generare caz nou (simulare senzor)
p_ix = np.random.uniform(200, 800)
p_iy = np.random.uniform(200, 800)
v_i = np.abs(np.sin(p_ix / 200.0)) * 100.0
a_i = np.abs(np.cos(v_i / 20.0)) * 50.0

# Alegem un defect la întâmplare
scenariu = np.random.choice([0, 1, 2])
if scenariu == 0: err = 0.5   # Mică
elif scenariu == 1: err = 12.0 # Medie
else: err = 60.0              # Mare

p_rx = p_ix + np.random.normal(err, err/4)
p_ry = p_iy + np.random.normal(err, err/4)
v_r = v_i + np.random.normal(err/3, 1)
a_r = a_i + np.random.normal(err/5, 0.5)

# PREGĂTIRE DATE (Preprocesare reală)
input_raw = np.array([[p_ix, p_iy, p_rx, p_ry, v_i, v_r, a_i, a_r]])
input_scaled = scaler.transform(input_raw)

# INFERENȚĂ (Modelul prezice)
pred_prob = model.predict(input_scaled)
clasa_idx = np.argmax(pred_prob)

clase = ['Precizie MARE (OK)', 'Precizie MEDIE (Warn)', 'Precizie MICĂ (Critical)']
culori = ['green', 'orange', 'red']

print(f"Scenariu Real Generat: Clasa {scenariu}")
print(f"Predicție Model: {clase[clasa_idx]} (Prob: {pred_prob[0][clasa_idx]*100:.1f}%)")

# VIZUALIZARE
plt.figure(figsize=(7, 6))
plt.scatter(p_ix, p_iy, c='green', s=200, label='Referință (Ideal)', edgecolors='black')
plt.scatter(p_rx, p_ry, c='red', marker='x', s=200, label='Măsurat (Real)', linewidth=3)
plt.plot([p_ix, p_rx], [p_iy, p_ry], 'k--', alpha=0.5, label='Eroare')

plt.title(f"LIVE INFERENCE\nDiagnostic AI: {clase[clasa_idx]}", color=culori[clasa_idx], fontweight='bold')
plt.xlabel("X [mm]"); plt.ylabel("Y [mm]")
plt.legend(); plt.grid(True)
plt.show()