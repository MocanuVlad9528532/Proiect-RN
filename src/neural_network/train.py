import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, f1_score, accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# --- CONFIGURARE CĂI (PATHS) ---
# Găsim folderul rădăcină al proiectului dinamic
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(BASE_DIR) # Adăugăm la path pentru importuri

# Importăm funcțiile din celălalt fișier
from src.preprocessing.combine_datasets import genereaza_set_date, augmenteaza_prin_jitter

# Definim căile de ieșire
DIRS = {
    'models': os.path.join(BASE_DIR, 'models'),
    'results': os.path.join(BASE_DIR, 'results'),
    'docs': os.path.join(BASE_DIR, 'docs'),
    'data': os.path.join(BASE_DIR, 'data', 'generated')
}
for d in DIRS.values():
    if not os.path.exists(d): os.makedirs(d)

FILES = {
    'model': os.path.join(DIRS['models'], 'trained_model.h5'),
    'scaler': os.path.join(DIRS['models'], 'scaler_spdt.gz'), # Salvăm scalerul în models pt simplitate
    'csv_data': os.path.join(DIRS['data'], 'dataset_final.csv'),
    'history': os.path.join(DIRS['results'], 'training_history.csv'),
    'loss_img': os.path.join(DIRS['docs'], 'loss_curve.png'),
    'conf_matrix': os.path.join(DIRS['docs'], 'confusion_matrix.png')
}

# --- 1. PREGĂTIRE DATE ---
print("=== ETAPA 5: START ANTRENARE ===")
np.random.seed(42); tf.random.set_seed(42)

X, Y_simplu = genereaza_set_date(6000)

# Salvare CSV
df = pd.DataFrame(X, columns=['PI_X','PI_Y','PR_X','PR_Y','VI','VR','AI','AR'])
df['Clasa'] = Y_simplu
df.to_csv(FILES['csv_data'], index=False)

Y = to_categorical(Y_simplu, num_classes=3)

# Split Stratificat
X_train, X_temp, y_train, y_temp = train_test_split(X, Y, test_size=0.30, random_state=42, stratify=Y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)

# Scalare
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, FILES['scaler'])
print(f"[OK] Scaler salvat în: {FILES['scaler']}")

# Augmentare
X_train_final, y_train_final = augmenteaza_prin_jitter(X_train_scaled, y_train)

# --- 2. MODELARE ---
model = Sequential([
    Dense(32, input_dim=8, activation='relu'),
    Dense(16, activation='relu'),
    Dense(3, activation='softmax')
])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001, verbose=1)
]

history = model.fit(
    X_train_final, y_train_final, 
    epochs=50, 
    batch_size=32, 
    validation_data=(X_val_scaled, y_val),
    callbacks=callbacks, 
    verbose=1
)

# --- 3. SALVARE REZULTATE ---
# CSV History
pd.DataFrame(history.history).to_csv(FILES['history'])
print(f"[OK] Istoric salvat în: {FILES['history']}")

# Grafic Loss
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss Curve'); plt.xlabel('Epoch'); plt.ylabel('Loss'); plt.legend(); plt.grid(True)
plt.savefig(FILES['loss_img'])
plt.close()
print(f"[OK] Grafic salvat în: {FILES['loss_img']}")

# Evaluare & Matrice Confuzie
y_pred = np.argmax(model.predict(X_test_scaled), axis=1)
y_true = np.argmax(y_test, axis=1)
acc = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred, average='macro')

plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Mare', 'Medie', 'Mica'])
disp.plot(cmap='Blues', values_format='d')
plt.title(f"Confusion Matrix\nAcc: {acc:.2f}, F1: {f1:.2f}")
plt.savefig(FILES['conf_matrix'], bbox_inches='tight')
plt.close()
print(f"[OK] Matrice Confuzie salvată în: {FILES['conf_matrix']}")

model.save(FILES['model'])
print(f"[OK] Model salvat în: {FILES['model']}")
print(f"=== RESULT: Accuracy={acc:.4f} | F1={f1:.4f} ===")