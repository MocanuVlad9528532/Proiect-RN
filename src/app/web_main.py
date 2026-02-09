import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import joblib
import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(
    page_title="SPDT - Robot Diagnosis",
    page_icon="🤖",
    layout="wide"
)

# --- CĂI CĂTRE MODELE ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'trained_model.h5')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler_spdt.gz')

# --- ÎNCĂRCARE MODEL (Cu Cache pentru viteză) ---
@st.cache_resource
def incarca_resurse():
    if not os.path.exists(MODEL_PATH):
        return None, None
    try:
        model = load_model(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    except Exception as e:
        st.error(f"Eroare la încărcare: {e}")
        return None, None

model, scaler = incarca_resurse()

# --- TITLU ȘI DESCRIERE ---
st.title("🤖 Sistem de Diagnoză Predictivă (SPDT)")
st.markdown("""
Această aplicație utilizează o **Rețea Neuronală** pentru a detecta anomaliile cinematice ale unui robot industrial.
Introduceți coordonatele comandate vs. cele măsurate pentru a primi un diagnostic.
""")
st.divider()

if model is None:
    st.error("⚠️ NU AM GĂSIT MODELUL! Rulează întâi `train.py`.")
    st.stop()

# --- COLOANE PENTRU INPUT ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Comandă (Ideal)")
    xi = st.number_input("Poziția X Ideal [mm]", value=500.0, step=1.0, format="%.1f")
    yi = st.number_input("Poziția Y Ideal [mm]", value=500.0, step=1.0, format="%.1f")

with col2:
    st.subheader("📡 Senzor (Real)")
    # Buton rapid pentru generare random
    if st.button("🎲 Generează Caz Random"):
        base_x = np.random.uniform(200, 800)
        base_y = np.random.uniform(200, 800)
        scenariu = np.random.choice(['ok', 'warn', 'crit'])
        defect = np.random.uniform(0.1, 4.0) if scenariu == 'ok' else (np.random.uniform(5.0, 18.0) if scenariu == 'warn' else np.random.uniform(25.0, 80.0))
        xr_val = base_x + np.random.normal(defect, 1.0)
        yr_val = base_y + np.random.normal(defect, 1.0)
    else:
        # Valori default (sau user input)
        xr_val = 500.0
        yr_val = 500.0

    # Inputurile reale (le lăsăm editabile)
    # Folosim session_state pentru a putea actualiza valorile din buton
    if 'xr_key' not in st.session_state: st.session_state.xr_key = xr_val
    if 'yr_key' not in st.session_state: st.session_state.yr_key = yr_val

    # Dacă s-a apăsat butonul random, actualizăm valorile afișate
    xr = st.number_input("Poziția X Real [mm]", value=float(xr_val), step=1.0, format="%.1f")
    yr = st.number_input("Poziția Y Real [mm]", value=float(yr_val), step=1.0, format="%.1f")

# --- BUTON DE ACȚIUNE ---
st.markdown("---")
buton_diagnoza = st.button("🔍 ANALIZEAZĂ TRAIECTORIA", type="primary", use_container_width=True)

if buton_diagnoza:
    # 1. Calcul Fizică (Preprocesare)
    v_i = np.abs(np.sin(xi / 200.0)) * 100.0
    a_i = np.abs(np.cos(v_i / 20.0)) * 50.0
    err_dist = np.sqrt((xi-xr)**2 + (yi-yr)**2)
    v_r = v_i + (err_dist / 2.0)
    a_r = a_i + (err_dist / 4.0)

    # 2. Predicție AI
    inp = np.array([[xi, yi, xr, yr, v_i, v_r, a_i, a_r]])
    inp_scaled = scaler.transform(inp)
    pred = model.predict(inp_scaled)
    cls_idx = np.argmax(pred)
    prob = pred[0][cls_idx] * 100

    # 3. Afișare Rezultate
    labels = ['NORMAL (OK)', 'WARNING (Uzură)', 'CRITICAL (Defect)']
    
    # Coloane rezultat: Stânga Text, Dreapta Grafic
    rez_col1, rez_col2 = st.columns([1, 2])

    with rez_col1:
        st.subheader("Rezultat Diagnoză")
        if cls_idx == 0:
            st.success(f"### ✅ {labels[0]}")
        elif cls_idx == 1:
            st.warning(f"### ⚠️ {labels[1]}")
        else:
            st.error(f"### 🛑 {labels[2]}")
        
        st.info(f"**Încredere AI:** {prob:.2f}%")
        st.write(f"**Eroare Poziție:** {err_dist:.2f} mm")
        st.write(f"**Viteză Estimată:** {v_r:.2f} mm/s")

    with rez_col2:
        # Generare Grafic Matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(xi, yi, c='green', s=200, label='Ideal', edgecolors='black', zorder=5)
        ax.scatter(xr, yr, c='red', marker='X', s=200, label='Real', zorder=5)
        ax.plot([xi, xr], [yi, yr], 'k--', alpha=0.5, label='Eroare')
        
        # Cercuri toleranță
        c1 = plt.Circle((xi, yi), 5, color='green', fill=False, linestyle=':', label='Limita OK')
        c2 = plt.Circle((xi, yi), 20, color='orange', fill=False, linestyle=':', label='Limita Warn')
        ax.add_patch(c1)
        ax.add_patch(c2)
        
        ax.set_title("Vizualizare Digital Twin")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # Trimitem graficul în pagina web
        st.pyplot(fig)