import numpy as np

def genereaza_set_date(n_samples=6000):
    """
    Generează date sintetice care respectă EXACT fizica din main.py.
    """
    # 1. Generăm coordonatele IDEALE (PI_X, PI_Y) random între 0 și 1000 mm
    # Acestea simulează comenzile date robotului
    pi_x = np.random.uniform(0, 1000, n_samples)
    pi_y = np.random.uniform(0, 1000, n_samples)

    # 2. Calculăm Cinematică IDEALĂ (Viteza si Accelerația teoretică)
    # FORMULE DIN MAIN.PY:
    # v_i = abs(sin(xi / 200)) * 100
    # a_i = abs(cos(vi / 20)) * 50
    v_i = np.abs(np.sin(pi_x / 200.0)) * 100.0
    a_i = np.abs(np.cos(v_i / 20.0)) * 50.0

    # 3. Introducem DEFECTE (Erori de poziționare)
    # Împărțim datele în 3 clase echilibrate
    y = np.zeros(n_samples)
    noise_magnitude = np.zeros(n_samples)

    # Indexi pentru fiecare clasă
    idx_ok = range(0, n_samples // 3)
    idx_warn = range(n_samples // 3, 2 * n_samples // 3)
    idx_crit = range(2 * n_samples // 3, n_samples)

    # CLASA 0: NORMAL (Eroare mică, 0 - 5 mm) -> Zona Verde din Grafic
    y[idx_ok] = 0
    noise_magnitude[idx_ok] = np.random.uniform(0, 4.5, len(idx_ok))

    # CLASA 1: WARNING (Eroare medie, 5 - 20 mm) -> Zona Portocalie
    y[idx_warn] = 1
    noise_magnitude[idx_warn] = np.random.uniform(5.5, 19.5, len(idx_warn))

    # CLASA 2: CRITICAL (Eroare mare, > 20 mm) -> Zona Roșie
    y[idx_crit] = 2
    noise_magnitude[idx_crit] = np.random.uniform(21.0, 100.0, len(idx_crit))

    # 4. Generăm coordonatele REALE (PR_X, PR_Y)
    # Adăugăm zgomotul (eroarea) pe o direcție random
    angle = np.random.uniform(0, 2 * np.pi, n_samples)
    pr_x = pi_x + noise_magnitude * np.cos(angle)
    pr_y = pi_y + noise_magnitude * np.sin(angle)

    # Recalculăm distanța exactă (pentru consistență matematică)
    err_dist = np.sqrt((pi_x - pr_x)**2 + (pi_y - pr_y)**2)

    # 5. Calculăm Cinematică REALĂ (Senzori)
    # FORMULE DIN MAIN.PY:
    # v_r = v_i + (err_dist / 3.0)
    # a_r = a_i + (err_dist / 5.0)
    v_r = v_i + (err_dist / 3.0)
    # Adăugăm și un mic zgomot de senzor (jitter) pentru realism
    v_r += np.random.normal(0, 0.5, n_samples) 
    
    a_r = a_i + (err_dist / 5.0)
    a_r += np.random.normal(0, 0.2, n_samples)

    # 6. Împachetăm totul într-o matrice X (Features)
    # Ordinea coloanelor: PI_X, PI_Y, PR_X, PR_Y, VI, VR, AI, AR
    X = np.column_stack((pi_x, pi_y, pr_x, pr_y, v_i, v_r, a_i, a_r))

    print(f"--> [DATA GEN] Generat {n_samples} mostre. Distribuție clase: {np.bincount(y.astype(int))}")
    return X, y

def augmenteaza_prin_jitter(X, y, noise_level=0.01):
    """
    Adaugă zgomot fin peste datele existente pentru a face modelul mai robust.
    """
    # Creăm zgomotul
    X_noise = X + np.random.normal(0, noise_level, X.shape)
    
    # Concatenăm datele originale cu cele zgomotoase (Vertical Stack)
    X_aug = np.vstack((X, X_noise))
    
    # CORECTARE: Folosim vstack și pentru y, deoarece y este deja One-Hot Encoded (matrice)
    y_aug = np.vstack((y, y))
    
    print(f"--> [AUGMENT] Date duplicate cu jitter. Total: {X_aug.shape[0]}")
    return X_aug, y_aug