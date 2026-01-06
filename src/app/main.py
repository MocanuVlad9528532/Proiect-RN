import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import joblib
from tensorflow.keras.models import load_model

# --- CONFIGURARE CĂI (PATHS) ---
# Acest bloc este critic: ne ajută să găsim modelul indiferent de unde rulăm scriptul
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # Folderul src/app
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR)) # Folderul rădăcină (PROIECT)

# Construim căile absolute către resurse
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'trained_model.h5')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler_spdt.gz')

# Verificăm dacă fișierele există înainte să crăpe programul
if not os.path.exists(MODEL_PATH):
    print(f"EROARE CRITICĂ: Nu găsesc modelul la: {MODEL_PATH}")
    print("SFAT: Rulează întâi 'python src/neural_network/train.py'!")
    sys.exit()

print("--> Încărcare sistem AI...")
try:
    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print(f"Eroare la încărcare: {e}")
    sys.exit()

print("\n=== LIVE DEMO SPDT (Interfață Operator) ===")
# Oprim seed-ul pentru a avea cazuri diferite la fiecare rulare
np.random.seed(None)

# 1. GENERARE CAZ SIMULAT (Senzori)
p_ix = np.random.uniform(200, 800); p_iy = np.random.uniform(200, 800)
v_i = np.abs(np.sin(p_ix/200))*100; a_i = np.abs(np.cos(v_i/20))*50

# Alegem un scenariu random
scenariu = np.random.choice([0, 1, 2])
if scenariu == 0: err = 0.5   # OK
elif scenariu == 1: err = 12.0 # Warning
else: err = 60.0              # Critical

# Adăugăm zgomotul specific scenariului
p_rx = p_ix + np.random.normal(err, err/4)
p_ry = p_iy + np.random.normal(err, err/4)
v_r = v_i + np.random.normal(err/3, 1)
a_r = a_i + np.random.normal(err/5, 0.5)

# 2. INFERENȚĂ (AI)
inp = np.array([[p_ix, p_iy, p_rx, p_ry, v_i, v_r, a_i, a_r]])
inp_scaled = scaler.transform(inp)
pred = model.predict(inp_scaled)
cls_idx = np.argmax(pred)

# Etichete pentru afișare
labels = ['OK (Precizie Mare)', 'WARN (Precizie Medie)', 'CRITICAL (Precizie Mică)']
colors = ['green', 'orange', 'red']

print(f"Scenariu Generat (Realitate): {labels[scenariu]}")
print(f"Diagnostic AI (Predicție):    {labels[cls_idx]} (Probabilitate: {pred[0][cls_idx]*100:.1f}%)")

# 3. VIZUALIZARE GRAFICĂ
plt.figure(figsize=(7, 7))
# Punctul Ideal
plt.scatter(p_ix, p_iy, c='green', s=150, label='Referință (Ideal)', edgecolors='k', zorder=5)
# Punctul Real
plt.scatter(p_rx, p_ry, c='red', marker='x', s=150, label='Măsurat (Real)', linewidth=3, zorder=5)
# Linia de eroare
plt.plot([p_ix, p_rx], [p_iy, p_ry], 'k--', alpha=0.5, label='Abatere')

# Cercuri de toleranță (vizual)
circle1 = plt.Circle((p_ix, p_iy), 5, color='green', fill=False, linestyle=':', label='Limita OK')
circle2 = plt.Circle((p_ix, p_iy), 20, color='orange', fill=False, linestyle=':', label='Limita Warn')
plt.gca().add_patch(circle1)
plt.gca().add_patch(circle2)

plt.title(f"MONITORIZARE LIVE\nDiagnostic: {labels[cls_idx]}", color=colors[cls_idx], fontweight='bold', fontsize=12)
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlabel("Coordonata X [mm]")
plt.ylabel("Coordonata Y [mm]")

# Afișare
plt.tight_layout()
plt.show()