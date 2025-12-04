# 📘 README – Etapa 4: Arhitectura Completă a Aplicației SIA bazată pe Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Mocanu Vlad-Cristian  
**https://github.com/MocanuVlad9528532/Proiect-RN.git**
**Data:** 12/4/2025 
---

## Scopul Etapei 4

Această etapă corespunde punctului **5. Dezvoltarea arhitecturii aplicației software bazată pe RN** din lista de 9 etape - slide 2 **RN Specificatii proiect.pdf**.

**Trebuie să livrați un SCHELET COMPLET și FUNCȚIONAL al întregului Sistem cu Inteligență Artificială (SIA). In acest stadiu modelul RN este doar definit și compilat (fără antrenare serioasă).**

### IMPORTANT - Ce înseamnă "schelet funcțional":

 **CE TREBUIE SĂ FUNCȚIONEZE:**
- Toate modulele pornesc fără erori
- Pipeline-ul complet rulează end-to-end (de la date → până la output UI)
- Modelul RN este definit și compilat (arhitectura există)
- Web Service/UI primește input și returnează output

 **CE NU E NECESAR ÎN ETAPA 4:**
- Model RN antrenat cu performanță bună
- Hiperparametri optimizați
- Acuratețe mare pe test set
- Web Service/UI cu funcționalități avansate

**Scopul anti-plagiat:** Nu puteți copia un notebook + model pre-antrenat de pe internet, pentru că modelul vostru este NEANTRENAT în această etapă. Demonstrați că înțelegeți arhitectura și că ați construit sistemul de la zero.

---

##  Livrabile Obligatorii

### 1. Tabelul Nevoie Reală → Soluție SIA → Modul Software (max ½ pagină)
Completați in acest readme tabelul următor cu **minimum 2-3 rânduri** care leagă nevoia identificată în Etapa 1-2 cu modulele software pe care le construiți (metrici măsurabile obligatoriu):

| **Nevoie reală concretă** | **Cum o rezolvă SIA-ul vostru** | **Modul software responsabil** |
|---------------------------|--------------------------------|--------------------------------|
| Diagnza automata a abaterolor cinematice ale robotuli| Analiză dinamică prin Rețele Neuronale (< 50 ms cu > 98% acuratețe) | Modul predictive + Preprocesare
| Reducerea timplui de nefunctionare neplanificat ( downtime) cauzat de uzura | Identificae timpurie a deradarii permormantei ( reducere estimată 20% costuri mentenanță ) | Modul Simulare Live + Logica decizie
| Vizualizarea intuitive a erorii pentru operatorii umani | Generare "Digital Twin" simplificat (Ideal vs Real)(interpretare vizuală instantanee a abaterii (eroare afișată în mm)) | Modul vizualizare(Matplotlib)

**Instrucțiuni:**
- Fiți concreti (nu vagi): "detectare fisuri sudură" ✓, "îmbunătățire proces" ✗
- Specificați metrici măsurabile: "< 2 secunde", "> 95% acuratețe", "reducere 20%"
- Legați fiecare nevoie de modulele software pe care le dezvoltați

---

### 2. Contribuția Voastră Originală la Setul de Date – MINIM 40% din Totalul Observațiilor Finale

Întregul set de date utilizat pentru antrenarea și testarea rețelei neuronale a fost generat integral (100%) prin simulare software proprie, folosind scriptul Python dezvoltat în cadrul proiectului. Nu au fost utilizate seturi de date externe (Kaggle, UCI, etc.).Metodologia de generare:S-a implementat un generator algoritmic care simulează comportamentul cinematic al unui robot (Poziție, Viteză, Accelerație), aplicând perturbații stocastice (zgomot Gaussian) controlate pentru a sintetiza cele 3 clase de precizie:Clasa Mare: Zgomot redus (x aprox. 0.5 mm)Clasa Medie: Zgomot moderat (x aprox 12 mm)Clasa Mică: Zgomot ridicat (x aprox 60 mm)

#### Tipuri de contribuții acceptate (exemple din inginerie):

Alegeți UNA sau MAI MULTE dintre variantele de mai jos și **demonstrați clar în repository**:

| **Tip contribuție** | **Exemple concrete din inginerie** | **Dovada minimă cerută** |
|---------------------|-------------------------------------|--------------------------|

| Date generate prin simulare fizică | Simulare cinematică completă (Poziție, Viteză, Accelerație) a traiectoriei robotului, cu injectare de zgomot Gaussian variabil pentru a modela matematic cele 3 stări de degradare mecanică (Normal, Uzură Medie, Defect Critic) | Script Python (genereaza_set_date) funcțional și comentat. ; Fișierul baza_de_date_robot.csv cu 6000 eșantioane. ; Graficul "Vizualizare Traiectorie" care compară vizual traiectoria Ideală vs. Reală, validând parametrii de zgomot aleși.

#### Declarație obligatorie în README:

Scrieți clar în acest README (Secțiunea 2):

### Contribuția originală la setul de date:

**Total observații finale:** 6,000 (după Etapa 3 + Etapa 4)
**Observații originale:** 6,000 (100%)

**Tipul contribuției:**
[X] Date generate prin simulare fizică
[ ] Date achiziționate cu senzori proprii
[ ] Etichetare/adnotare manuală
[ ] Date sintetice prin metode avansate

**Descriere detaliată:**
Setul de date a fost generat integral printr-un algoritm de simulare cinematică implementat în Python (folosind biblioteca NumPy). S-a modelat comportamentul dinamic al unui braț robotic industrial prin generarea a 6.000 de perechi de vectori de stare (Poziție, Viteză, Accelerație), reprezentând comparativ traiectoria "Ideală" (referința matematică) și traiectoria "Reală" (afectată de perturbații stocastice).

Metoda de generare utilizează distribuții de probabilitate Gaussiană (Normală) pentru a injecta zgomot specific în datele ideale, simulând astfel trei stări distincte de funcționare, imposibil de obținut echilibrat din date istorice reale: Funcționare Optimă (zgomot $\sigma \approx 0.5$ mm), Uzură Medie (zgomot $\sigma \approx 12$ mm) și Defect Critic (zgomot $\sigma \approx 60$ mm). Această abordare a permis crearea unui set de date perfect echilibrat (stratificat), eliminând problema "Class Imbalance".

Parametrii simulării au fost calibrați pentru a respecta limite fizice realiste (viteză max 100 mm/s, accelerație max 50 mm/s²), iar etichetarea (Labeling) s-a realizat automat în momentul generării, garantând o acuratețe de 100% a etichetelor de antrenare ("Ground Truth").

**Locația codului:** `proiect_final_v2.py` (funcția `genereaza_set_date`)
**Locația datelor:** `data/generated/baza_de_date_robot.csv`

**Dovezi:**
- Grafic comparativ: [Inserați aici screenshot-ul cu Vizualizare Traiectorie - Punct Verde vs Roșu]
- Setup experimental: Nu este cazul (Simulare Software)
- Tabel statistici: Vezi fișierul `baza_de_date_robot.csv` și Matricea de Confuzie generată la rulare.

#### Exemple pentru "contribuție originală":
-Simulări fizice realiste cu ecuații și parametri justificați  
-Date reale achiziționate cu senzori proprii (setup documentat)  
-Augmentări avansate cu justificare fizică (ex: simulare perspective camera industrială)  


#### Atenție - Ce NU este considerat "contribuție originală":

- Augmentări simple (rotații, flips, crop) pe date publice  
- Aplicare filtre standard (Gaussian blur, contrast) pe imagini publice  
- Normalizare/standardizare (aceasta e preprocesare, nu generare)  
- Subset dintr-un dataset public (ex: selectat 40% din ImageNet)


---

### 3. Diagrama State Machine a Întregului Sistem (OBLIGATORIE)

**Cerințe:**
- **Minimum 4-6 stări clare** cu tranziții între ele
- **Formate acceptate:** PNG/SVG, pptx, draw.io 
- **Locație:** `docs/state_machine.*` (orice extensie)
- **Legendă obligatorie:** 1-2 paragrafe în acest README: "De ce ați ales acest State Machine pentru nevoia voastră?"



IDLE → INITIALIZE_PARAMS → SIMULATE_AND_LOG (CSV) → PREPROCESS_DATA (Scaler) →
      ↓
MLP_TRAINING (Backpropagation) → EVALUATE_MODEL (Confusion Matrix) →
      ↓
SAVE_MODEL (.h5) → GENERATE_LIVE_SCENARIO (Random) →
      ↓
RN_INFERENCE (Forward Prop) → DECISION_LOGIC (Argmax) →
      │
      ├─ [Precizie Mare] ──→ DISPLAY_GREEN_STATUS ──┐
      ├─ [Precizie Medie] ─→ DISPLAY_YELLOW_WARN ───┤
      └─ [Precizie Mică] ──→ DISPLAY_RED_ALERT ─────┘
               ↓
        WAIT_USER_CLOSE → STOP


### Legendă State Machine: De ce am ales acest flux?

Am proiectat o mașină cu stări finite (FSM) secvențială, specifică sistemelor de **Mentenanță Predictivă bazate pe Simulare (Digital Twin)**. Arhitectura a fost aleasă pentru a separa clar faza de **Învățare (Training)** — care este intensivă computațional și se execută o singură dată (sau periodic) — de faza de **Infernță (Diagnoză)** — care trebuie să fie ultra-rapidă (<50ms) pentru monitorizarea în timp real.

Fluxul începe cu starea **SIMULATE_AND_LOG**, esențială pentru proiectul nostru deoarece garantează date de antrenare perfect echilibrate și salvează "Baza de Date" (CSV) pentru auditabilitate. Tranziția către **MLP_TRAINING** include automatizarea preprocesării (Normalizare), asigurând că modelul primește date curate.

În faza critică de **LIVE_DIAGNOSIS**, sistemul nu doar clasifică starea, ci intră într-o sub-stare de **VISUALIZATION_HMI**, generând feedback vizual imediat (Verde/Roșu) pentru operator. Starea finală include salvarea modelului pentru persistență, permițând sistemului să fie repornit direct în faza de inferență în iterațiile viitoare.


### Justificarea State Machine-ului ales:

Am ales arhitectura de **Monitorizare Predictivă bazată pe Digital Twin (Simulare)** pentru că proiectul nostru vizează **diagnoza automată a abaterilor cinematice** (conform nevoii identificate în Tabelul 1), separând complet faza de învățare (computațional intensivă) de faza de execuție (timp real).

Stările principale sunt:
1. **[DATA_GENERATION_LOG]:** Simulare cinematică a 6000 de eșantioane, injectare zgomot Gaussian specific claselor și scrierea bazei de date în format CSV (Audit Trail).
2. **[PREPROCESS_PIPELINE]:** Curățarea datelor, normalizarea vectorilor de intrare (Min-Max Scaling [0,1]) și codificarea etichetelor (One-Hot Encoding) pentru compatibilitate cu MLP.
3. **[MLP_TRAINING]:** Antrenarea iterativă a rețelei (Backpropagation) timp de 20 epoci, validarea pe setul de test și salvarea greutăților (.h5) pentru persistență.
4. **[LIVE_INFERENCE]:** Starea operațională ("Producție") unde sistemul preia un scenariu nou, aplică scaler-ul salvat și execută inferența (Forward Propagation) în < 10ms.
5. **[HMI_VISUALIZATION]:** Randarea grafică a "Digital Twin-ului" (Punct Verde vs. Roșu) și afișarea deciziei de diagnoză pentru operator.

Tranzițiile critice sunt:
- **[MLP_TRAINING] → [SAVE_MODEL]:** Se execută automat doar după convergența funcției de cost (Loss) și finalizarea epocilor, garantând un model stabil.
- **[INFERENCE] → [ALERT_STATE]:** Se declanșează instantaneu când probabilitatea clasei "Precizie Mică" este dominantă (`argmax == 2`), semnalând o defecțiune critică.

Starea **ERROR / SAFE_FALLBACK** este esențială pentru că în contextul aplicației noastre industriale, datele de intrare pot fi corupte (ex: valori NaN de la senzori defecți) sau fișierul modelului poate lipsi. În acest caz, sistemul trebuie să refuze predicția și să intre într-o stare de siguranță (Oprire Robot) în loc să genereze o traiectorie eronată.

Bucla de feedback este implementată vizual în starea **HMI_VISUALIZATION**: rezultatul inferenței este afișat grafic operatorului (Matrice de Confuzie și Traiectorie), permițând validarea umană rapidă înainte de a reporni procesul sau a solicita mentenanță.

---

### 4. Scheletul Complet al celor 3 Module Cerute la Curs (slide 7)

Toate cele 3 module trebuie să **pornească și să ruleze fără erori** la predare. Nu trebuie să fie perfecte, dar trebuie să demonstreze că înțelegeți arhitectura.

| **Modul** | **Python (exemple tehnologii)** | **LabVIEW** | **Cerință minimă funcțională (la predare)** |
|-----------|----------------------------------|-------------|----------------------------------------------|
| **1. Data Logging / Acquisition** | `src/data_acquisition/` | LLB cu VI-uri de generare/achiziție | **MUST:** Produce CSV cu datele voastre (inclusiv cele 40% originale). Cod rulează fără erori și generează minimum 100 samples demonstrative. |
| **2. Neural Network Module** | `src/neural_network/model.py` sau folder dedicat | LLB cu VI-uri RN | **MUST:** Modelul RN definit, compilat, poate fi încărcat. **NOT required:** Model antrenat cu performanță bună (poate avea weights random/inițializați). |
| **3. Web Service / UI** | Streamlit, Gradio, FastAPI, Flask, Dash | WebVI sau Web Publishing Tool | **MUST:** Primește input de la user și afișează un output. **NOT required:** UI frumos, funcționalități avansate. |

#### Detalii per modul:

#### **Modul 1: Data Logging / Acquisition**

**Funcționalități obligatorii:**
- [ ] Cod rulează fără erori: `python src/data_acquisition/generate.py` sau echivalent LabVIEW
- [ ] Generează CSV în format compatibil cu preprocesarea din Etapa 3
- [ ] Include minimum 40% date originale în dataset-ul final
- [ ] Documentație în cod: ce date generează, cu ce parametri

#### **Modul 2: Neural Network Module**

**Funcționalități obligatorii:**
- [ ] Arhitectură RN definită și compilată fără erori
- [ ] Model poate fi salvat și reîncărcat
- [ ] Include justificare pentru arhitectura aleasă (în docstring sau README)
- [ ] **NU trebuie antrenat** cu performanță bună (weights pot fi random)


#### **Modul 3: Web Service / UI**

**Funcționalități MINIME obligatorii:**
- [ ] Propunere Interfață ce primește input de la user (formular, file upload, sau API endpoint)
- [ ] Includeți un screenshot demonstrativ în `docs/screenshots/`

**Ce NU e necesar în Etapa 4:**
- UI frumos/profesionist cu grafică avansată
- Funcționalități multiple (istorice, comparații, statistici)
- Predicții corecte (modelul e neantrenat, e normal să fie incorect)
- Deployment în cloud sau server de producție

**Scop:** Prima demonstrație că pipeline-ul end-to-end funcționează: input user → preprocess → model → output.


## Structura Repository-ului la Finalul Etapei 4 (OBLIGATORIE)

**Verificare consistență cu Etapa 3:**

```
proiect-rn-[Mocanu Vlad-Cristian]/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── generated/  # Date originale
│   ├── train/
│   ├── validation/
│   └── test/
├── src/
│   ├── data_acquisition/
│   ├── preprocessing/  # Din Etapa 3
│   ├── neural_network/
│   └── app/  # UI schelet
├── docs/
│   ├── state_machine.*           #(state_machine.png sau state_machine.pptx sau state_machine.drawio)
│   └── [alte dovezi]
├── models/  # Untrained model
├── config/
├── README.md
├── README_Etapa3.md              # (deja existent)
├── README_Etapa4_Arhitectura_SIA.md              # ← acest fișier completat (în rădăcină)
└── requirements.txt  # Sau .lvproj
```

**Diferențe față de Etapa 3:**
- Adăugat `data/generated/` pentru contribuția dvs originală
- Adăugat `src/data_acquisition/` - MODUL 1
- Adăugat `src/neural_network/` - MODUL 2
- Adăugat `src/app/` - MODUL 3
- Adăugat `models/` pentru model neantrenat
- Adăugat `docs/state_machine.png` - OBLIGATORIU
- Adăugat `docs/screenshots/` pentru demonstrație UI

---

## Checklist Final – Bifați Totul Înainte de Predare

### Documentație și Structură
- [ ] Tabelul Nevoie → Soluție → Modul complet (minimum 2 rânduri cu exemple concrete completate in README_Etapa4_Arhitectura_SIA.md)
- [ ] Declarație contribuție 40% date originale completată în README_Etapa4_Arhitectura_SIA.md
- [ ] Cod generare/achiziție date funcțional și documentat
- [ ] Dovezi contribuție originală: grafice + log + statistici în `docs/`
- [ ] Diagrama State Machine creată și salvată în `docs/state_machine.*`
- [ ] Legendă State Machine scrisă în README_Etapa4_Arhitectura_SIA.md (minimum 1-2 paragrafe cu justificare)
- [ ] Repository structurat conform modelului de mai sus (verificat consistență cu Etapa 3)

### Modul 1: Data Logging / Acquisition
- [ ] Cod rulează fără erori (`python src/data_acquisition/...` sau echivalent LabVIEW)
- [ ] Produce minimum 40% date originale din dataset-ul final
- [ ] CSV generat în format compatibil cu preprocesarea din Etapa 3
- [ ] Documentație în `src/data_acquisition/README.md` cu:
  - [ ] Metodă de generare/achiziție explicată
  - [ ] Parametri folosiți (frecvență, durată, zgomot, etc.)
  - [ ] Justificare relevanță date pentru problema voastră
- [ ] Fișiere în `data/generated/` conform structurii

### Modul 2: Neural Network
- [ ] Arhitectură RN definită și documentată în cod (docstring detaliat) - versiunea inițială 
- [ ] README în `src/neural_network/` cu detalii arhitectură curentă

### Modul 3: Web Service / UI
- [ ] Propunere Interfață ce pornește fără erori (comanda de lansare testată)
- [ ] Screenshot demonstrativ în `docs/screenshots/ui_demo.png`
- [ ] README în `src/app/` cu instrucțiuni lansare (comenzi exacte)

---

**Predarea se face prin commit pe GitHub cu mesajul:**  
`"Etapa 4 completă - Arhitectură SIA funcțională"`

**Tag obligatoriu:**  
`git tag -a v0.4-architecture -m "Etapa 4 - Skeleton complet SIA"`


