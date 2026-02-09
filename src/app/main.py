import os
import sys
import time
import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import joblib
import tkinter as tk
from tkinter import messagebox
from tensorflow.keras.models import load_model

# =========================================================
# 1. CONFIGURARE PROIECT & CĂI
# =========================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'trained_model.h5')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler_spdt.gz')
LOG_PATH = os.path.join(BASE_DIR, 'results', 'inference_logs.csv')

# Verificări inițiale
if not os.path.exists(MODEL_PATH):
    messagebox.showerror("Eroare Critică", "Lipsesc fișierele modelului (Etapa 5)!")
    sys.exit()

print("--> [INIT] Încărcare resurse AI...")
try:
    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    messagebox.showerror("Eroare", f"Model corupt: {e}")
    sys.exit()

# Inițializare fișier log
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Comanda_X", "Comanda_Y", "Real_X", "Real_Y", "Diagnostic", "Probabilitate", "Latenta_ms"])

# =========================================================
# 2. LOGICA BUSINESS & STATE MACHINE
# =========================================================
def log_inference(data_row):
    with open(LOG_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)
    print(f"-> [LOG] Salvat în {LOG_PATH}")

def ruleaza_diagnoza():
    start_time = time.time()
    
    try:
        # 1. ACHIZIȚIE DATE (UI)
        xi = float(entry_xi.get())
        yi = float(entry_yi.get())
        xr = float(entry_xr.get())
        yr = float(entry_yr.get())

        # 2. PREPROCESARE (Calcul cinematic derivat)
        # --- Aici este matematica "invizibilă" ---
        v_i = np.abs(np.sin(xi / 200.0)) * 100.0
        a_i = np.abs(np.cos(v_i / 20.0)) * 50.0
        
        err_dist = np.sqrt((xi-xr)**2 + (yi-yr)**2)
        
        v_r = v_i + (err_dist / 3.0) 
        a_r = a_i + (err_dist / 5.0)
        # -----------------------------------------

        # UPDATE UI: Afișăm valorile calculate
        lbl_vi.config(text=f"{v_i:.2f} mm/s")
        lbl_vr.config(text=f"{v_r:.2f} mm/s", fg="red" if abs(v_r - v_i) > 5 else "black")
        lbl_ai.config(text=f"{a_i:.2f} mm/s²")
        lbl_ar.config(text=f"{a_r:.2f} mm/s²", fg="red" if abs(a_r - a_i) > 2 else "black")

        # 3. INFERENȚĂ (RN)
        inp = np.array([[xi, yi, xr, yr, v_i, v_r, a_i, a_r]])
        inp_scaled = scaler.transform(inp)
        
        pred = model.predict(inp_scaled, verbose=0)
        cls_idx = np.argmax(pred)
        prob = pred[0][cls_idx] * 100

        # 4. STATE MACHINE UPDATE
        labels = ['OK (Normal)', 'WARNING (Uzura)', 'CRITICAL (Defect)']
        colors_ui = ['green', 'orange', 'red']
        
        if prob < 60.0:
            final_label = "INCERT (Analiză necesară)"
            final_color = "gray"
        else:
            final_label = labels[cls_idx]
            final_color = colors_ui[cls_idx]

        latency = (time.time() - start_time) * 1000

        # 5. UI UPDATE & ALERTĂ
        lbl_rezultat.config(text=f"Stare: {final_label}", fg=final_color)
        lbl_detalii.config(text=f"Încredere: {prob:.1f}% | Latență: {latency:.2f} ms")

        # 6. DATA LOGGING
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_inference([timestamp, xi, yi, xr, yr, final_label, f"{prob:.1f}%", f"{latency:.2f}"])

        genereaza_grafic(xi, yi, xr, yr, final_label, final_color)

    except ValueError:
        messagebox.showwarning("Input Invalid", "Introduceți valori numerice!")

def genereaza_grafic(xi, yi, xr, yr, diagnostic, culoare):
    plt.figure(figsize=(5, 5))
    plt.scatter(xi, yi, c='green', s=100, label='Ideal', zorder=5)
    plt.scatter(xr, yr, c='red', marker='x', s=100, label='Real', zorder=5)
    plt.plot([xi, xr], [yi, yr], 'k--', alpha=0.5, label='Eroare')
    
    plt.gca().add_patch(plt.Circle((xi, yi), 5, color='green', fill=False, linestyle=':'))
    plt.gca().add_patch(plt.Circle((xi, yi), 20, color='orange', fill=False, linestyle=':'))

    plt.title(f"DIAGNOZĂ VIZUALĂ\n{diagnostic}", color=culoare if culoare != 'gray' else 'black', fontweight='bold')
    plt.legend(loc='upper right', fontsize='small')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def auto_fill():
    base_x = np.random.uniform(200, 800)
    base_y = np.random.uniform(200, 800)
    defect = np.random.choice([0.5, 12.0, 60.0])
    
    real_x = base_x + np.random.normal(defect, defect/4)
    real_y = base_y + np.random.normal(defect, defect/4)

    entry_xi.delete(0, tk.END); entry_xi.insert(0, f"{base_x:.1f}")
    entry_yi.delete(0, tk.END); entry_yi.insert(0, f"{base_y:.1f}")
    entry_xr.delete(0, tk.END); entry_xr.insert(0, f"{real_x:.1f}")
    entry_yr.delete(0, tk.END); entry_yr.insert(0, f"{real_y:.1f}")

# =========================================================
# 3. INTERFAȚA GRAFICĂ (GUI)
# =========================================================
root = tk.Tk()
root.title("SPDT v1.1 - Extended Monitor")
root.geometry("480x700") # Am mărit puțin fereastra

tk.Label(root, text="Sistem Diagnoză Predictivă", font=("Segoe UI", 16, "bold"), pady=15).pack()

frame_main = tk.Frame(root, relief=tk.RIDGE, borderwidth=2, padx=10, pady=10)
frame_main.pack(fill=tk.BOTH, expand=True, padx=20)

# --- INPUTURI ---
tk.Label(frame_main, text="Coordonate (IDEAL)", fg="green", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
tk.Label(frame_main, text="X [mm]:").grid(row=1, column=0); entry_xi = tk.Entry(frame_main); entry_xi.grid(row=1, column=1)
tk.Label(frame_main, text="Y [mm]:").grid(row=2, column=0); entry_yi = tk.Entry(frame_main); entry_yi.grid(row=2, column=1)

tk.Label(frame_main, text="Coordonate (REAL)", fg="red", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=2, pady=5)
tk.Label(frame_main, text="X [mm]:").grid(row=4, column=0); entry_xr = tk.Entry(frame_main); entry_xr.grid(row=4, column=1)
tk.Label(frame_main, text="Y [mm]:").grid(row=5, column=0); entry_yr = tk.Entry(frame_main); entry_yr.grid(row=5, column=1)

# --- NOUL PANOU DE PARAMETRI INTERNI ---
tk.Frame(frame_main, height=2, bg="#dddddd").grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)
tk.Label(frame_main, text="Cinematică Calculată (Intern)", fg="blue", font=("Arial", 10, "bold")).grid(row=7, column=0, columnspan=2, pady=2)

tk.Label(frame_main, text="Viteza Ideală:").grid(row=8, column=0, sticky="e")
lbl_vi = tk.Label(frame_main, text="-", font=("Consolas", 9)); lbl_vi.grid(row=8, column=1, sticky="w")

tk.Label(frame_main, text="Viteza Reală:").grid(row=9, column=0, sticky="e")
lbl_vr = tk.Label(frame_main, text="-", font=("Consolas", 9)); lbl_vr.grid(row=9, column=1, sticky="w")

tk.Label(frame_main, text="Accel. Ideală:").grid(row=10, column=0, sticky="e")
lbl_ai = tk.Label(frame_main, text="-", font=("Consolas", 9)); lbl_ai.grid(row=10, column=1, sticky="w")

tk.Label(frame_main, text="Accel. Reală:").grid(row=11, column=0, sticky="e")
lbl_ar = tk.Label(frame_main, text="-", font=("Consolas", 9)); lbl_ar.grid(row=11, column=1, sticky="w")

# --- CONTROL ---
tk.Frame(frame_main, height=2, bg="#dddddd").grid(row=12, column=0, columnspan=2, sticky="ew", pady=10)
tk.Button(frame_main, text="🎲 Simulare Senzor (Auto)", command=auto_fill, bg="#dddddd").grid(row=13, column=0, columnspan=2, pady=5, sticky="ew")
tk.Button(frame_main, text="⚡ EXECUTA DIAGNOZA", bg="#007bff", fg="white", font=("Arial", 11, "bold"), command=ruleaza_diagnoza, height=2).grid(row=14, column=0, columnspan=2, sticky="ew", pady=5)

# --- REZULTATE ---
lbl_rezultat = tk.Label(root, text="System Ready", font=("Segoe UI", 14, "bold"), fg="#333", pady=10)
lbl_rezultat.pack()
lbl_detalii = tk.Label(root, text="Așteptare date...", font=("Consolas", 10), fg="gray")
lbl_detalii.pack()

tk.Label(root, text=f"Log path: results/inference_logs.csv", font=("Arial", 7), fg="gray").pack(side=tk.BOTTOM, pady=5)

root.mainloop()