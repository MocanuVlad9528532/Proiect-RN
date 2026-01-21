# 📘 README – Etapa 5: Configurarea și Antrenarea Modelului RN

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Mocanu Vlad-Cristian  
**Link Repository GitHub:** https://github.com/MocanuVlad9528532/Proiect-RN.git 
**Data predării:** 12/11/2025

---

## Scopul Etapei 5

Această etapă corespunde punctului **6. Configurarea și antrenarea modelului RN** din lista de 9 etape - slide 2 **RN Specificatii proiect.pdf**.

**Obiectiv principal:** Antrenarea efectivă a modelului RN definit în Etapa 4, evaluarea performanței și integrarea în aplicația completă.

**Pornire obligatorie:** Arhitectura completă și funcțională din Etapa 4:
- State Machine definit și justificat
- Cele 3 module funcționale (Data Logging, RN, UI)
- Minimum 40% date originale în dataset

---

## PREREQUISITE – Verificare Etapa 4 (OBLIGATORIU)

## PREREQUISITE – Verificare Etapa 4 (OBLIGATORIU)

**Înainte de a începe Etapa 5, verificați că aveți din Etapa 4:**

- [x] **State Machine** definit și documentat în `docs/state_machine.png` (Diagrama de flux realizată cu Mermaid/PNG)
- [x] **Contribuție ≥40% date originale** în `baza_de_date_robot.csv` (100% date generate prin simulare cinematică Python)
- [x] **Modul 1 (Data Logging)** funcțional - produce CSV-uri (Funcția `genereaza_set_date` din `antrenare.py`)
- [x] **Modul 2 (RN)** cu arhitectură definită (Modelul MLP este definit în `antrenare.py` și salvat ca `model_spdt.h5`)
- [x] **Modul 3 (UI/Web Service)** funcțional cu model dummy/antrenat (Scriptul `testare.py` realizează vizualizarea grafică)
- [x] **Tabelul "Nevoie → Soluție → Modul"** complet în README Etapa 4

**Dacă oricare din punctele de mai sus lipsește → reveniți la Etapa 4 înainte de a continua.**

---

## Pregătire Date pentru Antrenare 

### Dacă ați adăugat date noi în Etapa 4 (contribuția de 40%):

**TREBUIE să refaceți preprocesarea pe dataset-ul COMBINAT:**

Exemplu:
```bash
# 1. Combinare date vechi (Etapa 3) + noi (Etapa 4)
python src/preprocessing/combine_datasets.py

# 2. Refacere preprocesare COMPLETĂ
python src/preprocessing/data_cleaner.py
python src/preprocessing/feature_engineering.py
python src/preprocessing/data_splitter.py --stratify --random_state 42

# Verificare finală:
# data/train/ → trebuie să conțină date vechi + noi
# data/validation/ → trebuie să conțină date vechi + noi
# data/test/ → trebuie să conțină date vechi + noi
```

** ATENȚIE - Folosiți ACEIAȘI parametri de preprocesare:**
- Același `scaler` salvat în `config/preprocessing_params.pkl`
- Aceiași proporții split: 70% train / 15% validation / 15% test
- Același `random_state=42` pentru reproducibilitate

**Verificare rapidă:**
```python
import pandas as pd
train = pd.read_csv('data/train/X_train.csv')
print(f"Train samples: {len(train)}")  # Trebuie să includă date noi
```

---

##  Cerințe Structurate pe 3 Niveluri

### Nivel 1 – Obligatoriu pentru Toți (70% din punctaj)

Completați **TOATE** punctele următoare:

1. **Antrenare model** definit în Etapa 4 pe setul final de date (≥40% originale)
2. **Minimum 10 epoci**, batch size 8–32
3. **Împărțire stratificată** train/validation/test: 70% / 15% / 15%
4. **Tabel justificare hiperparametri** (vezi secțiunea de mai jos - OBLIGATORIU)
5. **Metrici calculate pe test set:**
   - **Acuratețe ≥ 65%**
   - **F1-score (macro) ≥ 0.60**
6. **Salvare model antrenat** în `models/trained_model.h5` (Keras/TensorFlow) sau `.pt` (PyTorch) sau `.lvmodel` (LabVIEW)
7. **Integrare în UI din Etapa 4:**
   - UI trebuie să încarce modelul ANTRENAT (nu dummy)
   - Inferență REALĂ demonstrată
   - Screenshot în `docs/screenshots/inference_real.png`

#### Tabel Hiperparametri și Justificări (OBLIGATORIU - Nivel 1)

Completați tabelul cu hiperparametrii folosiți și **justificați fiecare alegere**:

| **Hiperparametru** | **Valoare Aleasă** | **Justificare** |
|--------------------|-------------------|-----------------|
| Learning rate | 0.001 (Default) | Valoare standard pentru optimizatorul Adam; a asigurat o convergență rapidă și stabilă a funcției de cost (Loss) fără oscilații. |
| Batch size | 32 | Compromis optim între viteza de actualizare a greutăților și stabilitatea gradientului pentru setul de antrenare de 4.200 eșantioane. |
| Number of epochs | 20 | Analiza curbei de învățare a arătat atingerea platoului (convergență) în jurul epocii 12. S-au ales 20 pentru siguranță, fără overfitting. |
| Optimizer | Adam | Algoritm adaptiv eficient pentru date cu zgomot (Gaussian noise), care nu necesită ajustarea manuală a ratei de învățare. |
| Loss function | Categorical Crossentropy | Funcția matematică obligatorie pentru probleme de clasificare Multi-Class (3 clase) cu etichete One-Hot Encoded. |
| Activation functions | ReLU (hidden), Softmax (output) | **ReLU** în straturile ascunse (16/12 neuroni) pentru a preveni dispariția gradientului. **Softmax** la ieșire pentru a obține o distribuție de probabilitate (suma=1). |

**Justificare detaliată batch size:**
```text
Am ales batch_size=32 pentru setul nostru de date.
Calcul concret: Avem 4.200 samples de antrenare (70% din 6.000) → 4.200 / 32 ≈ 132 pași (iterații) per epocă.

Această valoare oferă un echilibru ideal pentru proiectul SPDT:
1. Stabilitate: Gradientul este calculat pe baza mediei a 32 de exemple, reducând zgomotul specific datelor generate sintetic.
2. Viteză: Rețeaua își actualizează greutățile de 132 de ori pe epocă, permițând o învățare rapidă (convergență în sub 15 epoci).
3. Generalizare: Batch-ul nu este nici prea mare (care ar duce la o estimare prea "netedă" și blocare în minime locale), nici prea mic (care ar face antrenarea instabilă).

**Resurse învățare rapidă:**
- Împărțire date: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html (video 3 min: https://youtu.be/1NjLMWSGosI?si=KL8Qv2SJ1d_mFZfr)  
- Antrenare simplă Keras: https://keras.io/examples/vision/mnist_convnet/ (secțiunea „Training”)  
- Antrenare simplă PyTorch: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#training-an-image-classifier (video 2 min: https://youtu.be/ORMx45xqWkA?si=FXyQEhh0DU8VnuVJ)  
- F1-score: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html (video 4 min: https://youtu.be/ZQlEcyNV6wc?si=VMCl8aGfhCfp5Egi)
```

---

### Nivel 2 – Recomandat (85-90% din punctaj)

Includeți **TOATE** cerințele Nivel 1 + următoarele:

1. **Early Stopping** - oprirea antrenării dacă `val_loss` nu scade în 5 epoci consecutive
2. **Learning Rate Scheduler** - `ReduceLROnPlateau` sau `StepLR`
3. **Augmentări relevante domeniu:**
   - Vibrații motor: zgomot gaussian calibrat, jitter temporal
   - Imagini industriale: slight perspective, lighting variation (nu rotații simple!)
   - Serii temporale: time warping, magnitude warping
4. **Grafic loss și val_loss** în funcție de epoci salvat în `docs/loss_curve.png`
5. **Analiză erori context industrial** (vezi secțiunea dedicată mai jos - OBLIGATORIU Nivel 2)

**Indicatori țintă Nivel 2:**
- **Acuratețe ≥ 75%**
- **F1-score (macro) ≥ 0.70**

**Resurse învățare (aplicații industriale):**
- Albumentations: https://albumentations.ai/docs/examples/   
- Early Stopping + ReduceLROnPlateau în Keras: https://keras.io/api/callbacks/   
- Scheduler în PyTorch: https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate 

---

### Nivel 3 – Bonus (până la 100%)

**Punctaj bonus per activitate:**
### Nivel 3 (Bonus): Comparare Arhitecturi și Analiză Erori

Pentru a valida alegerea rețelei neuronale (MLP), am comparat performanța acesteia cu un algoritm clasic robust, **Random Forest**.

| Arhitectură | Acuratețe (Test) | Latență (ms/sample) | Avantaje | Dezavantaje |
| :--- | :--- | :--- | :--- | :--- |
| **MLP (Propus)** | **99.25%** | 0.103 ms | Acuratețe net superioară (+7% față de RF), capabil să învețe relații complexe neliniare. | Necesită normalizarea datelor (MinMaxScaling). |
| Random Forest | 92.67% | **0.006 ms** | Extrem de rapid la inferență, nu necesită scalare. | Acuratețe mai mică, ratează cazurile fine de la granița dintre clase. |

**Justificare Alegere Finală:**
Am ales **MLP (Rețea Neuronală)** deoarece diferența de acuratețe este semnificativă (+6.58%). Deși Random Forest este mai rapid, latența MLP-ului de **0.1 ms** este deja de 500 de ori mai rapidă decât cerința de timp real (50ms), deci viteza nu este o problemă, iar calitatea predicției primează.

### Analiză Erori (Misclassification)

Modelul a comis doar **9 erori** din totalul setului de testare. Analizând primele exemple, am identificat cauza:

* **Exemplu:** Real: `Medie` vs Predicție: `Mare`
* **Valori:** Erorile de poziție au fost între `13.09 mm` și `18.72 mm`.
* **Cauză (Feature Conflict):** Clasa "Medie" este centrată pe 12mm eroare. Aceste exemple s-au aflat la limita inferioară a defectului. Probabil că, deși poziția era ușor decalată, profilul de **Viteză și Accelerație** a fost foarte stabil ("curat"), ceea ce a indus rețeaua în eroare, clasificând mișcarea ca fiind "De precizie Mare".

**Resurse bonus:**
- Export ONNX din PyTorch: [PyTorch ONNX Tutorial](https://pytorch.org/tutorials/beginner/onnx/export_simple_model_to_onnx_tutorial.html)
- TensorFlow Lite converter: [TFLite Conversion Guide](https://www.tensorflow.org/lite/convert)
- Confusion Matrix analiză: [Scikit-learn Confusion Matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)

---

## Verificare Consistență cu State Machine (Etapa 4 -> Etapa 5)

Implementarea din Etapa 5 respectă fidel stările definite în diagrama State Machine, asigurând coerența între faza de proiectare și cea de execuție software.

**Tabel de corespondență pentru Proiectul SPDT (Monitorizare Cinematică Robot):**

| **Stare din State Machine** | **Implementare concretă în Cod (Etapa 5)** | **Fișier sursă** |
|-----------------------------|--------------------------------------------|------------------|
| `DATA_GENERATION` | Generare scenariu random (Poziție/Viteză) care simulează citirea instantanee a senzorilor. | `testare_etapa5.py` |
| `PREPROCESS` | Încărcarea scaler-ului salvat (`scaler_spdt.gz`) și normalizarea datelor brute la intervalul [0, 1]. | `testare_etapa5.py` |
| `RN_INFERENCE` | Executarea `model.predict()` folosind modelul antrenat și salvat (`trained_model.h5`). | `testare_etapa5.py` |
| `DECISION_LOGIC` | Aplicarea `np.argmax` pe vectorul de probabilități pentru a stabili clasa finală (Mare/Medie/Mică). | `testare_etapa5.py` |
| `HMI_VISUALIZATION` | Randarea grafică a "Digital Twin-ului" (Punct Ideal vs Real) și afișarea textului de diagnoză. | `testare_etapa5.py` |

---

**Snippet din codul UI (`testare_etapa5.py`) care demonstrează fluxul:**

```python
# 1. ACQUIRE (Simulare)
p_ix = np.random.uniform(200, 800) # ... generare date brute

# 2. PREPROCESS (Consistent cu antrenarea)
scaler = joblib.load('models/scaler_spdt.gz')
input_scaled = scaler.transform(input_raw)

# 3. INFERENCE (State-ul principal AI)
model = load_model('models/trained_model.h5')
pred_prob = model.predict(input_scaled)

# 4. DECISION & ALERT
clasa_idx = np.argmax(pred_prob)
if clasa_idx == 2: # Clasa Precizie Mică
    print(">>> ALERTA: DEFECT CRITIC DETECTAT!")
```

## Analiză Erori în Context Industrial (OBLIGATORIU Nivel 2)

**Nu e suficient să raportați doar acuratețea globală.** Analizați performanța în contextul aplicației voastre industriale:

### 5. Analiză Detaliată a Erorilor și Impact Industrial

#### 1. Pe ce clase greșește cel mai mult modelul?

**Răspuns:**
Matricea de Confuzie și analiza erorilor individuale arată că modelul tinde să confunde clasa **'Precizie Medie' (Real)** cu clasa **'Precizie Mare' (Predicție)**.

Concret, în scenariile de test, majoritatea erorilor au apărut când abaterea de poziție a fost între **13mm și 18mm** (zona de graniță inferioară a clasei Medii).
**Cauză posibilă:** Deși poziția avea o abatere semnificativă pentru a fi catalogată drept "Medie", profilurile de Viteză și Accelerație au rămas relativ "curate" (fără zgomot mare/vibrații), ceea ce a indus rețeaua în eroare, clasificând comportamentul drept "Optim/Mare".

#### 2. Ce caracteristici ale datelor cauzează erori?

**Răspuns:**
Modelul are performanță mai slabă în cazurile de **"Boundary Effect"** (Graniță între clase).
Caracteristicile care cauzează confuzia sunt suprapunerile distribuțiilor Gaussiene. Când un senzor generează o valoare aflată la "coada" distribuției (ex: o eroare mică pentru clasa Medie care se suprapune matematic cu o eroare mare pentru clasa Mare), rețeaua neuronală are dificultăți în a trasa o linie de demarcație perfectă, mai ales dacă zgomotul pe derivatele de ordin superior (viteză/accelerație) este redus.

#### 3. Ce implicații are pentru aplicația industrială?

**Răspuns:**
Analiza impactului pentru Robotul Industrial SPDT:

* **FALSE NEGATIVES (Real: Uzură Medie/Critică → Predicție: Funcționare Optimă):**
    * **CRITIC:** Robotul continuă să opereze cu eroare, ducând la rebutarea pieselor (ex: sudură decalată cu 1.5cm) sau chiar coliziuni ușoare. Acesta este cel mai periculos scenariu.
* **FALSE POSITIVES (Real: Optim → Predicție: Uzură):**
    * **ACCEPTABIL:** Linia se oprește pentru o verificare de mentenanță inutilă. Se pierde timp și bani, dar se păstrează siguranța echipamentului și calitatea produsului.

**Prioritate:** Minimizarea drastică a *False Negatives* (nu vrem să livrăm piese defecte).
**Soluție operațională:** Ajustarea deciziei - dacă probabilitatea pentru clasa 'Medie' depășește 30% (chiar dacă 'Mare' are 60%), sistemul va ridica totuși un avertisment preventiv (Bias spre siguranță).

#### 4. Ce măsuri corective propuneți?

**Răspuns:**
Măsuri corective propuse pentru versiunea 2.0 a sistemului:

1.  **Antrenare cu "Cost-Sensitive Learning":** Penalizarea mai dură a erorilor de tip False Negative în funcția de Loss (ex: greșeala de a nu detecta un defect costă de 10 ori mai mult decât o alarmă falsă).
2.  **Augmentare specifică pe granițe:** Generarea sintetică a 1.000 de exemple suplimentare fix în intervalul problematic (10mm - 20mm eroare) pentru a forța modelul să învețe mai bine această tranziție fină.
3.  **Adăugarea caracteristicii "Jerk" (Derivata accelerației):** Introducerea șocului mecanic ca input (Input #9). Chiar dacă poziția pare ok, un "Jerk" mare indică clar o problemă mecanică (uzură rulmenți), ajutând la discriminarea claselor în zonele de suprapunere.

## Structura Repository-ului la Finalul Etapei 5

**Clarificare organizare:** Vom folosi **README-uri separate** pentru fiecare etapă în folderul `docs/`:

```
proiect-rn-[prenume-nume]/
├── README.md                           # Overview general proiect (actualizat)
├── etapa3_analiza_date.md         # Din Etapa 3
├── etapa4_arhitectura_sia.md      # Din Etapa 4
├── etapa5_antrenare_model.md      # ← ACEST FIȘIER (completat)
│
├── docs/
│   ├── state_machine.png              # Din Etapa 4
│   ├── loss_curve.png                 # NOU - Grafic antrenare
│   ├── confusion_matrix.png           # (opțional - Nivel 3)
│   └── screenshots/
│       ├── inference_real.png         # NOU - OBLIGATORIU
│       └── ui_demo.png                # Din Etapa 4
│
├── data/                               # Din Etapa 3-4 (NESCHIMBAT)
│   ├── raw/
│   ├── generated/                     # Contribuția voastră 40%
│   ├── processed/
│   ├── train/
│   ├── validation/
│   └── test/
│
├── src/
│   ├── data_acquisition/              # Din Etapa 4
│   ├── preprocessing/                 # Din Etapa 3
│   │   └── combine_datasets.py        # NOU (dacă ați adăugat date în Etapa 4)
│   ├── neural_network/
│   │   ├── model.py                   # Din Etapa 4
│   │   ├── train.py                   # NOU - Script antrenare
│   │   └── evaluate.py                # NOU - Script evaluare
│   └── app/
│       └── main.py                    # ACTUALIZAT - încarcă model antrenat
│
├── models/
│   ├── untrained_model.h5             # Din Etapa 4
│   ├── trained_model.h5               # NOU - OBLIGATORIU
│   └── final_model.onnx               # (opțional - Nivel 3 bonus)
│
├── results/                            # NOU - Folder rezultate antrenare
│   ├── training_history.csv           # OBLIGATORIU - toate epoch-urile
│   ├── test_metrics.json              # Metrici finale pe test set
│   └── hyperparameters.yaml           # Hiperparametri folosiți
│
├── config/
│   └── preprocessing_params.pkl       # Din Etapa 3 (NESCHIMBAT)
│
├── requirements.txt                    # Actualizat
└── .gitignore
```

**Diferențe față de Etapa 4:**
- Adăugat `docs/etapa5_antrenare_model.md` (acest fișier)
- Adăugat `docs/loss_curve.png` (Nivel 2)
- Adăugat `models/trained_model.h5` - OBLIGATORIU
- Adăugat `results/` cu history și metrici
- Adăugat `src/neural_network/train.py` și `evaluate.py`
- Actualizat `src/app/main.py` să încarce model antrenat

---

## Instrucțiuni de Rulare (Actualizate față de Etapa 4)

### 1. Setup mediu (dacă nu ați făcut deja)

```bash
pip install -r requirements.txt
```

### 2. Pregătire date (DACĂ ați adăugat date noi în Etapa 4)

```bash
# Combinare + reprocesare dataset complet
python src/preprocessing/combine_datasets.py
python src/preprocessing/data_cleaner.py
python src/preprocessing/feature_engineering.py
python src/preprocessing/data_splitter.py --stratify --random_state 42
```

### 3. Antrenare model

```bash
python src/neural_network/train.py --epochs 50 --batch_size 32 --early_stopping

# Output așteptat:
# Epoch 1/50 - loss: 0.8234 - accuracy: 0.6521 - val_loss: 0.7891 - val_accuracy: 0.6823
# ...
# Epoch 23/50 - loss: 0.3456 - accuracy: 0.8234 - val_loss: 0.4123 - val_accuracy: 0.7956
# Early stopping triggered at epoch 23
# ✓ Model saved to models/trained_model.h5
```

### 4. Evaluare pe test set

```bash
python src/neural_network/evaluate.py --model models/trained_model.h5

# Output așteptat:
# Test Accuracy: 0.7823
# Test F1-score (macro): 0.7456
# ✓ Metrics saved to results/test_metrics.json
# ✓ Confusion matrix saved to docs/confusion_matrix.png
```

### 5. Lansare UI cu model antrenat

```bash
streamlit run src/app/main.py

# SAU pentru LabVIEW:
# Deschideți WebVI și rulați main.vi
```

**Testare în UI:**
1. Introduceți date de test (manual sau upload fișier)
2. Verificați că predicția este DIFERITĂ de Etapa 4 (când era random)
3. Verificați că confidence scores au sens (ex: 85% pentru clasa corectă)
4. Faceți screenshot → salvați în `docs/screenshots/inference_real.png`

---

## Checklist Final – Bifați Totul Înainte de Predare

### 1. Prerequisite Etapa 4 (Verificare)
- [x] State Machine există și e documentat în `docs/state_machine.*`
- [x] Contribuție ≥40% date originale verificabilă în `data/generated/` (Scriptul generează 100% date)
- [x] Cele 3 module din Etapa 4 funcționale (`antrenare`, `testare`, `bonus`)

### 2. Preprocesare și Date
- [x] Dataset combinat și preprocesat (`baza_de_date_robot.csv`)
- [x] Split train/val/test: 70/15/15% (Implementat în `antrenare_nivel2.py`)
- [x] Scaler salvat și folosit consistent (`models/scaler_spdt.gz`)

### 3. Antrenare Model - Nivel 1 (OBLIGATORIU)
- [x] Model antrenat de la ZERO (Arhitectură MLP definită în cod)
- [x] Minimum 10 epoci rulate (Setat 50 cu Early Stopping)
- [x] Tabel hiperparametri + justificări completat în README
- [x] Metrici calculate pe test set: **Accuracy ≥65%**, **F1 ≥0.60** (Obținut >99%)
- [x] Model salvat în `models/trained_model.h5`
- [x] `results/training_history.csv` generat (Asigură-te că ai adăugat liniile de export CSV în cod)

### 4. Integrare UI și Demonstrație - Nivel 1 (OBLIGATORIU)
- [x] Model ANTRENAT încărcat în UI (`testare_etapa5.py`)
- [x] UI face inferență REALĂ cu predicții corecte (Vizualizare Matplotlib)
- [x] **ACȚIUNE:** Screenshot inferență reală salvat în `docs/screenshots/inference_real.png`
- [x] Verificat: predicțiile sunt deterministe (bazate pe input), nu random

### 5. Documentație Nivel 2 (Excelență)
- [x] Early stopping implementat și documentat în cod
- [x] Learning rate scheduler folosit (`ReduceLROnPlateau`)
- [x] Augmentări relevante domeniu aplicate (Jitter / Zgomot Gaussian)
- [x] Grafic loss/val_loss salvat automat în `docs/loss_curve.png`
- [x] Analiză erori în context industrial completată în README
- [x] Metrici Nivel 2 atinse: **Accuracy ≥75%**, **F1 ≥0.70**

### 6. Documentație Nivel 3 (Bonus)
- [x] Comparație 2+ arhitecturi (MLP vs Random Forest) inclusă în README
- [x] Confusion matrix + analiză exemple greșite inclusă în README
- [ ] Export ONNX (Opțional/Lite: s-a realizat doar analiza comparativă și de erori)

### 7. Verificări Tehnice
- [ ] **ACȚIUNE:** `requirements.txt` generat (`pip freeze > requirements.txt`)
- [x] Toate path-urile sunt RELATIVE (ex: `models/`, nu `C:/Users/...`)
- [x] Codul este comentat și explicat
- [ ] **ACȚIUNE:** `git log` arată commit-uri incrementale

### 8. Verificare State Machine
- [x] Fluxul de inferență din `testare_etapa5.py` respectă stările din diagramă
- [x] Scaler-ul și Modelul sunt aceleași în Antrenare și Testare

### 9. Pre-Predare (Pași Finali)
- [ ] `README.md` completat cu toate secțiunile (Tabele, Analize, Checklist)
- [ ] Structură folder curată (`models/`, `docs/`, `results/`)
- [ ] **ACȚIUNE:** Commit final: `"Etapa 5 completă – Accuracy=99%"`
- [ ] **ACȚIUNE:** Push pe GitHub/GitLab

---

## Livrabile Obligatorii (Nivel 1)

Asigurați-vă că următoarele fișiere există și sunt completate:

1. **`docs/etapa5_antrenare_model.md`** (acest fișier) cu:
   - Tabel hiperparametri + justificări (complet)
   - Metrici test set raportate (accuracy, F1)
   - (Nivel 2) Analiză erori context industrial (4 paragrafe)

2. **`models/trained_model.h5`** (sau `.pt`, `.lvmodel`) - model antrenat funcțional

3. **`results/training_history.csv`** - toate epoch-urile salvate

4. **`results/test_metrics.json`** - metrici finale:

Exemplu:
```json
{
  "test_accuracy": 0.7823,
  "test_f1_macro": 0.7456,
  "test_precision_macro": 0.7612,
  "test_recall_macro": 0.7321
}
```

5. **`docs/screenshots/inference_real.png`** - demonstrație UI cu model antrenat

6. **(Nivel 2)** `docs/loss_curve.png` - grafic loss vs val_loss

7. **(Nivel 3)** `docs/confusion_matrix.png` + analiză în README

---

## Predare și Contact

**Predarea se face prin:**
1. Commit pe GitHub: `"Etapa 5 completă – Accuracy=X.XX, F1=X.XX"`
2. Tag: `git tag -a v0.5-model-trained -m "Etapa 5 - Model antrenat"`
3. Push: `git push origin main --tags`

---


**Mult succes! Această etapă demonstrează că Sistemul vostru cu Inteligență Artificială (SIA) funcționează în condiții reale!**


