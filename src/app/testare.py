import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import joblib
from tensorflow.keras.models import load_model

# Configurare Căi
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'trained_model.h5')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler_spdt.gz')

if not os.path.exists(MODEL_PATH):
    print("EROARE: Rulează 'src/neural_network/train.py' întâi!"); exit()

print("--> Încărcare sistem AI...")
model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("\n=== LIVE DEMO SPDT ===")
# Generare caz random
p_ix = np.random.uniform(200, 800); p_iy = np.random.uniform(200, 800)
v_i = np.abs(np.sin(p_ix/200))*100; a_i = np.abs(np.cos(v_i/20))*50

scenariu = np.random.choice([0, 1, 2])
if scenariu == 0: err = 0.5 
elif scenariu == 1: err = 12.0
else: err = 60.0

p_rx = p_ix + np.random.normal(err, err/4)
p_ry = p_iy + np.random.normal(err, err/4)
v_r = v_i + np.random.normal(err/3, 1)
a_r = a_i + np.random.normal(err/5, 0.5)

# Inferență
inp = np.array([[p_ix, p_iy, p_rx, p_ry, v_i, v_r, a_i, a_r]])
inp_scaled = scaler.transform(inp)
pred = model.predict(inp_scaled)
cls_idx = np.argmax(pred)
labels = ['OK (Mare)', 'WARN (Medie)', 'CRITICAL (Mica)']
colors = ['green', 'orange', 'red']

print(f"Scenariu Generat: {labels[scenariu]}")
print(f"Diagnostic AI:    {labels[cls_idx]} (Prob: {pred[0][cls_idx]*100:.1f}%)")

# Vizualizare
plt.figure(figsize=(6,6))
plt.scatter(p_ix, p_iy, c='green', s=150, label='Ideal', edgecolors='k')
plt.scatter(p_rx, p_ry, c='red', marker='x', s=150, label='Real', linewidth=3)
plt.plot([p_ix, p_rx], [p_iy, p_ry], 'k--', alpha=0.5)
plt.title(f"Diagnostic: {labels[cls_idx]}", color=colors[cls_idx], fontweight='bold')
plt.legend(); plt.grid(True)
plt.show()