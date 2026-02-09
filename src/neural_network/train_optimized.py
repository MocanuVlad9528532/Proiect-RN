import tensorflow as tf
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ================= CONFIGURARE =================
MODEL_SAVE_PATH = 'models/optimized_model.h5'
INPUT_DIM = 8       # 8 Senzori
NUM_CLASSES = 3     # OK, WARNING, CRITICAL
EPOCHS = 50         # Maxim, dar se va opri mai devreme
BATCH_SIZE = 32

# ================= 1. GENERARE DATE SINTETICE (Simulare Dataset) =================
# Notă: Într-un caz real, aici ai încărca datele din CSV.
# Pentru a garanta că acest script rulează acum, generăm date "perfecte" pentru optimizare.
print("--- 1. Pregătire Date ---")

def generate_data(n_samples=2000):
    X = np.random.rand(n_samples, INPUT_DIM)
    y = np.zeros(n_samples, dtype=int)
    
    for i in range(n_samples):
        # Logica simplificată: Suma valorilor decide clasa
        score = np.sum(X[i])
        if score < 2.5:
            y[i] = 0 # OK
        elif score < 4.5:
            y[i] = 1 # WARNING
        else:
            y[i] = 2 # CRITICAL
            
            # OPTIMIZARE DATASET: Adăugăm zgomot controlat pentru robustețe
            X[i] += np.random.normal(0, 0.05, INPUT_DIM)
            
    return X, y

X, y = generate_data()

# Scalare (Standardizare) - Esențial pentru convergență rapidă
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split Train/Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Dataset size: {X_train.shape[0]} train / {X_test.shape[0]} test")

# ================= 2. DEFINIRE ARHITECTURĂ OPTIMIZATĂ =================
print("--- 2. Construire Model Optimizat ---")

model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(INPUT_DIM,)),
    
    # Strat 1: Complexitate medie + Regularizare
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.BatchNormalization(), # OPTIMIZARE: Stabilizează antrenarea
    tf.keras.layers.Dropout(0.3),         # OPTIMIZARE: Previne Overfitting
    
    # Strat 2: Reducere dimensiune
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2),         # OPTIMIZARE: Regularizare ușoară
    
    # Output: Softmax pentru probabilități
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

# Compilare cu Learning Rate Tuned
optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005) # LR mai mic pentru precizie

model.compile(optimizer=optimizer,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# ================= 3. CALLBACKS (Preventie Overfitting) =================
callbacks = [
    # Oprește antrenarea dacă nu mai învață timp de 5 epoci
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    
    # Salvează doar cea mai bună versiune a modelului
    tf.keras.callbacks.ModelCheckpoint(MODEL_SAVE_PATH, monitor='val_accuracy', save_best_only=True)
]

# ================= 4. ANTRENARE =================
print("--- 3. Start Antrenare (Optimization Process) ---")
history = model.fit(
    X_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_data=(X_test, y_test),
    callbacks=callbacks,
    verbose=1
)

# ================= 5. EVALUARE FINALĂ =================
print("--- 4. Rezultate Finale ---")
loss, acc = model.evaluate(X_test, y_test)
print(f"\n✅ FINAL TEST ACCURACY: {acc*100:.2f}%")
print(f"✅ Model optimizat salvat la: {MODEL_SAVE_PATH}")