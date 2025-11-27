import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay # [NOU] Pentru Matrice
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import os

# ==========================================
# 1. CONFIGURARE PARAMETRI PROIECT
# ==========================================
NUMAR_ESANTIOANE = 6000   
DIMENSIUNE_INPUT = 8      # [P_IX, P_IY, P_RX, P_RY, VI, VR, AI, AR]
DIMENSIUNE_OUTPUT = 3     # [Mare, Medie, Mica]
FISIER_MODEL = 'model_spdt.h5'
FISIER_DATE = 'baza_de_date_robot.csv'

# Setăm seed pentru stabilitate
np.random.seed(42)
tf.random.set_seed(42)

# ==========================================
# 2. FUNCȚII GENERARE DATE SIMULATE
# ==========================================
def genereaza_set_date(n_samples):
    print("Generare date simulate pentru antrenare...")
    
    P_IX = np.random.uniform(0, 1000, n_samples)
    P_IY = np.random.uniform(0, 1000, n_samples)
    
    V_I = np.abs(np.sin(P_IX / 200.0)) * 100.0 
    A_I = np.abs(np.cos(V_I / 20.0)) * 50.0

    X_data = []
    Y_labels = [] 

    segment = n_samples // 3

    # --- CLASA 1: PRECIZIE MARE ---
    for i in range(segment):
        err_p = np.random.normal(0, 0.5)
        err_v = np.random.normal(0, 0.2)
        err_a = np.random.normal(0, 0.1)
        row = [P_IX[i], P_IY[i], P_IX[i]+err_p, P_IY[i]+err_p, V_I[i], V_I[i]+err_v, A_I[i], A_I[i]+err_a]
        X_data.append(row)
        Y_labels.append(0) 

    # --- CLASA 2: PRECIZIE MEDIE ---
    for i in range(segment, segment*2):
        err_p = np.random.normal(12, 4.0)
        err_v = np.random.normal(5, 2.0)
        err_a = np.random.normal(2, 1.0)
        row = [P_IX[i], P_IY[i], P_IX[i]+err_p, P_IY[i]+err_p, V_I[i], V_I[i]+err_v, A_I[i], A_I[i]+err_a]
        X_data.append(row)
        Y_labels.append(1) 

    # --- CLASA 3: PRECIZIE MICĂ ---
    for i in range(segment*2, n_samples):
        err_p = np.random.normal(60, 15.0)
        err_v = np.random.normal(20, 5.0)
        err_a = np.random.normal(10, 3.0)
        row = [P_IX[i], P_IY[i], P_IX[i]+err_p, P_IY[i]+err_p, V_I[i], V_I[i]+err_v, A_I[i], A_I[i]+err_a]
        X_data.append(row)
        Y_labels.append(2) 

    X = np.array(X_data)
    return X, Y_labels

# ==========================================
# 3. MAIN - EXECUȚIA PROGRAMULUI
# ==========================================

# --- PASUL A: Generarea Datelor ---
X, Y_simplu = genereaza_set_date(NUMAR_ESANTIOANE)

# --- PASUL B: Salvarea CSV ---
print(f"Salvam baza de date in: {FISIER_DATE} ...")
nume_coloane = ['Poz_Ideal_X', 'Poz_Ideal_Y', 'Poz_Real_X', 'Poz_Real_Y', 'Vit_Ideal', 'Vit_Real', 'Acc_Ideal', 'Acc_Real']
df = pd.DataFrame(X, columns=nume_coloane)
mapare_nume = {0: 'Mare', 1: 'Medie', 2: 'Mica'}
df['Clasa_Precizie'] = [mapare_nume[y] for y in Y_simplu]
df.to_csv(FISIER_DATE, index=False)
print("--> Fisier CSV salvat!\n")

# --- PASUL C: Preprocesare ---
Y = to_categorical(Y_simplu, num_classes=3)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train) 
X_test_scaled = scaler.transform(X_test)       

# --- PASUL D: Crearea Modelului ---
model = Sequential([
    Dense(16, input_dim=DIMENSIUNE_INPUT, activation='relu', name='Strat_Intrare'),
    Dense(12, activation='relu', name='Strat_Ascuns'),
    Dense(DIMENSIUNE_OUTPUT, activation='softmax', name='Strat_Iesire')
])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# --- PASUL E: Antrenarea ---
print("Începe antrenarea...")
history = model.fit(X_train_scaled, y_train, epochs=20, batch_size=32, validation_data=(X_test_scaled, y_test), verbose=1)

# --- PASUL F: Grafice de Performanță ---
# 7.1 Graficul Acurateței
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Antrenare', linewidth=2)
plt.plot(history.history['val_accuracy'], label='Testare', linewidth=2)
plt.title('Evoluția Acurateței')
plt.xlabel('Epoci')
plt.ylabel('Acuratețe')
plt.legend()
plt.grid(True)

# 7.2 [NOU] Matricea de Confuzie
print("\nGenerare Matrice de Confuzie...")
plt.subplot(1, 2, 2)
# Facem predicții pe tot setul de test
y_pred_prob = model.predict(X_test_scaled)
y_pred_class = np.argmax(y_pred_prob, axis=1)
y_true_class = np.argmax(y_test, axis=1)

cm = confusion_matrix(y_true_class, y_pred_class)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Mare', 'Medie', 'Mică'])
disp.plot(ax=plt.gca(), cmap='Blues', values_format='d')
plt.title('Matricea de Confuzie (Unde greșește modelul?)')

plt.tight_layout()
plt.show() # Așteaptă închiderea graficelor

# Salvarea modelului
model.save(FISIER_MODEL)
print(f"\nModel salvat: {FISIER_MODEL}")

# ==========================================
# 9. DEMO PREDICTIE & VIZUALIZARE LIVE
# ==========================================
np.random.seed(None) # Resetăm seed-ul pentru random real

print("\n" + "="*40)
print("   SIMULARE LIVE - VIZUALIZARE GRAFICĂ")
print("="*40)

# Generare caz random
rand_p_x = np.random.uniform(200, 800) # Limităm zona pentru grafic mai clar
rand_p_y = np.random.uniform(200, 800)
rand_v_i = np.abs(np.sin(rand_p_x / 200.0)) * 100.0
rand_a_i = np.abs(np.cos(rand_v_i / 20.0)) * 50.0

scenariu_real = np.random.choice([0, 1, 2]) 
if scenariu_real == 0: 
    tip_scenariu = "NORMAL (Eroare minima)"
    err_p = np.random.normal(0, 0.5)
    err_v = np.random.normal(0, 0.2); err_a = np.random.normal(0, 0.1)
elif scenariu_real == 1: 
    tip_scenariu = "UZURA (Eroare medie)"
    err_p = np.random.normal(25, 5.0) # Am mărit puțin eroarea vizuală
    err_v = np.random.normal(5, 2.0); err_a = np.random.normal(2, 1.0)
else: 
    tip_scenariu = "DEFECT (Eroare grava)"
    err_p = np.random.normal(100, 20.0) # Am mărit eroarea pt impact vizual
    err_v = np.random.normal(20, 5.0); err_a = np.random.normal(10, 3.0)

rand_p_rx = rand_p_x + err_p
rand_p_ry = rand_p_y + err_p 
rand_v_r = rand_v_i + err_v
rand_a_r = rand_a_i + err_a

# Predicție
date_raw = np.array([[rand_p_x, rand_p_y, rand_p_rx, rand_p_ry, rand_v_i, rand_v_r, rand_a_i, rand_a_r]])
date_scaled = scaler.transform(date_raw)
pred = model.predict(date_scaled)
clasa_idx = np.argmax(pred) 
clase_text = ['Precizie Mare', 'Precizie Medie', 'Precizie Mică']
culori = ['green', 'orange', 'red'] # Culori pentru grafic

print(f"Scenariu: {tip_scenariu}")
print(f"Diferență Poziție: {abs(rand_p_x - rand_p_rx):.2f} mm")
print(f"DIAGNOSTIC AI: {clase_text[clasa_idx]}")

# --- 10.  VIZUALIZARE GRAFICĂ A PUNCTELOR ---
plt.figure(figsize=(6, 6))

# Desenăm punctul IDEAL (Verde, cerc plin)
plt.scatter(rand_p_x, rand_p_y, color='green', s=150, label='Poziție IDEALĂ', edgecolors='black', zorder=5)

# Desenăm punctul REAL (Roșu/Portocaliu, X)
plt.scatter(rand_p_rx, rand_p_ry, color='red', marker='x', s=150, linewidth=3, label='Poziție REALĂ', zorder=5)

# Desenăm o linie între ele pentru a vizualiza eroarea
plt.plot([rand_p_x, rand_p_rx], [rand_p_y, rand_p_ry], color='gray', linestyle='--', label='Eroare')

# Setări grafic
plt.xlim(0, 1000); plt.ylim(0, 1000)
plt.title(f"Vizualizare Traiectorie\nDiagnostic: {clase_text[clasa_idx]}", color=culori[clasa_idx], fontweight='bold', fontsize=14)
plt.xlabel("Coordonata X (mm)"); plt.ylabel("Coordonata Y (mm)")
plt.legend()
plt.grid(True, alpha=0.3)

print("Se deschide fereastra de vizualizare...")
plt.show()