# 📘 README – Etapa 3: Analiza și Pregătirea Setului de Date pentru Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Mocanu Vlad-Cristian 
**Data:** 20/11/2025  

---

## Introducere

Acest document descrie activitățile realizate în **Etapa 3**, în care se analizează și se preprocesează setul de date necesar proiectului „Rețele Neuronale". Scopul etapei este pregătirea corectă a datelor pentru instruirea modelului RN, respectând bunele practici privind calitatea, consistența și reproductibilitatea datelor.

---

##  1. Structura Repository-ului Github (versiunea Etapei 3)

```
project-name/
├── README.md
├── docs/
│   └── datasets/          # descriere seturi de date, surse, diagrame
├── data/
│   ├── raw/               # date brute
│   ├── processed/         # date curățate și transformate
│   ├── train/             # set de instruire
│   ├── validation/        # set de validare
│   └── test/              # set de testare
├── src/
│   ├── preprocessing/     # funcții pentru preprocesare
│   ├── data_acquisition/  # generare / achiziție date (dacă există)
│   └── neural_network/    # implementarea RN (în etapa următoare)
├── config/                # fișiere de configurare
└── requirements.txt       # dependențe Python (dacă aplicabil)
```

---

##  2. Descrierea Setului de Date

### 2.1 Sursa datelor

* **Origine:** Senzori Robot,simulare
* **Modul de achiziție:** ☐ Senzori reali / ✔ Simulare / ☐ Fișier extern / ☐ Generare programatică
* **Perioada / condițiile colectării:** Noiembrie 2025-Ianuarie 2026

### 2.2 Caracteristicile dataset-ului

* **Număr total de observații:6000
* **Număr de caracteristici (features):** 3
* **Tipuri de date:** ✔ Numerice / ☐ Categoriale / ☐ Temporale / ☐ Imagini
* **Format fișiere:** ☐ CSV / ✔ TXT / ☐ JSON / ☐ PNG / ☐ Altele: [...]

### 2.3 Descrierea fiecărei caracteristici

| **Caracteristică** | **Tip** | **Unitate** | **Descriere** | **Domeniu valori** |
|-------------------|---------|-------------|---------------|--------------------|
| acceleratie | numeric | mm/s^2 | Acceleratie robotului | 0–150 |
| pozitie | numeric | mm | Pozitia robotului | {x,y} |
| viteza | numeric | mm/s | Viteza robotului | 0-150 |


**Fișier recomandat:**  `data/README.md`

---

##  3. Analiza Exploratorie a Datelor (EDA) – Sintetic

### 3.1 Statistici descriptive aplicate

* **Medie, mediană, deviație standard** : Deoarece datele sunt generate uniform pentru traiectoria ideală, media pozițiilor este centrată în jurul valorii de 500 mm. Deviația standard a erorii variază în funcție de clasă: mică pentru 'Precizie Mare' și ridicată pentru 'Precizie Mică'
  
* **Min–max și quartile** : Domeniul valorilor de intrare este fixat prin parametrii de simulare: Poziție [0 - 1000] mm, Viteză [0 - 100] mm/s, Accelerație [0 - 50] mm/s². Nu există valori care să depășească aceste limite fizice impuse.
  
* **Distribuții pe caracteristici** (histograme) : Caracteristicile 'Ideale' urmează o distribuție uniformă (acoperă tot spațiul de lucru). Caracteristicile 'Reale' urmează o distribuție uniformă suprapusă cu un zgomot Gaussian (distribuție normală), specific fiecărei clase de eroare.
  
* **Identificarea outlierilor** (IQR / percentile) : În acest set de date, 'outlierii' (valorile cu abateri mari) nu sunt erori de date, ci reprezintă instanțele clasei 'Precizie Mică'. Acestea sunt esențiale pentru ca modelul să învețe să detecteze defectele.

### 3.2 Analiza calității datelor

* **Detectarea valorilor lipsă** (% pe coloană) : 0% valori lipsă. Fiind un set de date sintetic generat algoritmic, toate câmpurile sunt completate automat la generare. Nu necesită imputare.
  
* **Detectarea valorilor inconsistente sau eronate** : Nu există valori inconsistente (ex: viteză negativă sau accelerație infinită) deoarece funcțiile de generare folosesc np.abs() și limite fizice hard-codate. Datele respectă legile cinematice de bază.
  
* **Identificarea caracteristicilor redundante sau puternic corelate** : Există o corelație puternică (>0.9) între coloanele 'Ideal' și 'Real' corespunzătoare (ex: P_IX vs P_RX). Această redundanță este intenționată și necesară, deoarece diferența subtilă dintre ele (reziduul) este exact informația pe care Rețeaua Neuronală trebuie să o învețe.

### 3.3 Probleme identificate

[exemplu] Feature X are 8% valori lipsă:

Înlocuiește cu: "Diferențe majore de scară între caracteristici: Poziția are valori până la 1000, în timp ce Accelerația doar până la 50. Acest lucru impune obligatoriu Normalizarea (MinMax Scaling) înainte de antrenare."

[exemplu] Distribuția feature Y este puternic neuniformă:

Înlocuiește cu: "Distribuție perfect echilibrată a claselor: Nu există 'Class Imbalance'. Setul a fost generat forțat cu 33% eșantioane pentru fiecare dintre cele 3 clase (Mare, Medie, Mică), eliminând riscul de biasare a modelului."

[exemplu] Variabilitate ridicată în clase:

Înlocuiește cu: "Suprapunere marginală la granița claselor: Există o ușoară zonă de suprapunere probabilistică între erorile clasei 'Medie' și 'Mică', simulând incertitudinea reală a senzorilor, ceea ce poate duce la o eroare mică de clasificare la testare."

---

##  4. Preprocesarea Datelor

### 4.1 Curățarea datelor

  4.1 Curățarea datelor
Eliminare duplicatelor:

Nu a fost necesară o etapă explicită, deoarece datele sunt generate algoritmic cu o componentă de zgomot aleatoriu (Gaussian), ceea ce asigură unicitatea fiecărui vector de intrare.

Tratarea valorilor lipsă:

Procent valori lipsă: 0%.

Metodă: Nu se aplică (datele sunt complete prin construcție).

Tratarea outlierilor:

Nu s-a aplicat eliminarea outlierilor (ex: IQR), deoarece valorile extreme (erori mari de poziție) reprezintă tocmai clasa de interes "Precizie Mică". Eliminarea lor ar fi redus capacitatea modelului de a detecta defectele grave.

### 4.2 Transformarea caracteristicilor

   Normalizare:

Metodă: Min-Max Scaling (scalare în intervalul [0, 1]).

Motiv: Diferențele mari de scară între Poziție (0-1000 mm) și Accelerație (0-50 mm/s²) ar fi destabilizat antrenarea rețelei neuronale.

Implementare: S-a utilizat clasa MinMaxScaler din biblioteca Scikit-Learn.

Encoding pentru variabile categoriale:

Metodă: One-Hot Encoding.

Aplicare: Variabila țintă (eticheta clasei: 0, 1, 2) a fost transformată în vectori binari (ex: Clasa 0 -> [1, 0, 0]) folosind funcția to_categorical din Keras.

Ajustarea dezechilibrului de clasă:

Nu a fost necesară (not applicable). Setul de date a fost generat echilibrat din start (33% pentru fiecare clasă).

### 4.3 Structurarea seturilor de date

   Împărțire utilizată:

80% – Set de Antrenare (Training)

20% – Set de Testare (Testing)

(Validarea s-a făcut implicit pe setul de test în timpul antrenării prin parametrul validation_data).

Principii respectate:

Stratificare: Împărțirea a fost aleatorie, dar având un set mare și echilibrat, distribuția claselor s-a păstrat uniformă în ambele seturi.

Data Leakage (Scurgere de informație): S-a evitat prin calcularea parametrilor de scalare (fit) DOAR pe setul de antrenare, iar apoi s-a aplicat transformarea (transform) pe setul de test.

### 4.4 Salvarea rezultatelor preprocesării

   Date preprocesate:

Datele brute au fost salvate în fișierul dataset_final.csv pentru documentare.

Obiecte de preprocesare:

Obiectul scaler (MinMaxScaler) nu a fost salvat fizic în acest prototip, fiind re-inițializat la fiecare rulare, dar într-un mediu de producție ar fi salvat folosind biblioteca joblib.

---

##  5. Fișiere Generate în Această Etapă

* `data/raw/` – date brute
* `data/processed/` – date curățate & transformate
* `data/train/`, `data/validation/`, `data/test/` – seturi finale
* `src/preprocessing/` – codul de preprocesare
* `data/README.md` – descrierea dataset-ului

---

##  6. Stare Etapă (de completat de student)

- [x ] Structură repository configurată
- [x ] Dataset analizat (EDA realizată)
- [ x] Date preprocesate
- [ x] Seturi train/val/test generate
- [x ] Documentație actualizată în README + `data/README.md`

---
