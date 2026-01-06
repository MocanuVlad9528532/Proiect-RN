import numpy as np
import pandas as pd

def genereaza_set_date(n_samples):
    """ Generează date simulate cinematic """
    print("-> [DATA] Generare date simulate...")
    P_IX = np.random.uniform(0, 1000, n_samples)
    P_IY = np.random.uniform(0, 1000, n_samples)
    V_I = np.abs(np.sin(P_IX / 200.0)) * 100.0 
    A_I = np.abs(np.cos(V_I / 20.0)) * 50.0

    X_data = []
    Y_labels = [] 
    segment = n_samples // 3

    for i in range(n_samples):
        if i < segment: cls = 0; noise_lvl = 0.5   
        elif i < segment*2: cls = 1; noise_lvl = 12.0 
        else: cls = 2; noise_lvl = 60.0 

        row = [
            P_IX[i], P_IY[i], 
            P_IX[i] + np.random.normal(cls*10, noise_lvl), 
            P_IY[i] + np.random.normal(cls*10, noise_lvl), 
            V_I[i], 
            V_I[i] + np.random.normal(cls*2, noise_lvl/3), 
            A_I[i], 
            A_I[i] + np.random.normal(cls*1, noise_lvl/5)  
        ]
        X_data.append(row)
        Y_labels.append(cls)

    return np.array(X_data), np.array(Y_labels)

def augmenteaza_prin_jitter(X, y, noise_scale=0.01):
    """ Adaugă zgomot fin pentru a simula vibrații senzori """
    print(f"-> [DATA] AUGMENTARE: Aplicare Jitter pe {len(X)} exemple...")
    noise = np.random.normal(0, noise_scale, X.shape)
    X_aug = X + noise
    X_final = np.concatenate((X, X_aug), axis=0)
    y_final = np.concatenate((y, y), axis=0)
    return X_final, y_final