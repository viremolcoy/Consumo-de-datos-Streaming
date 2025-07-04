import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# === Cargar y preparar datos ===
df = pd.read_csv("datos_limpiados.csv")

# 🔧 NUEVAS FEATURES: cliente frecuencia, producto frecuencia
cliente_freq = df["cliente"].value_counts().to_dict()
producto_freq = df["producto"].value_counts().to_dict()
df["cliente_freq"] = df["cliente"].map(cliente_freq)
df["producto_freq"] = df["producto"].map(producto_freq)

# (Opcional: eliminar outliers extremos de monto o cantidad)
df = df[df["monto"] < df["monto"].quantile(0.98)]
df = df[df["cantidad"] < df["cantidad"].quantile(0.98)]

# === Definir variables
X = df[["cliente", "producto", "cantidad", "cliente_freq", "producto_freq"]]
y = df["monto"]

# === Codificar cliente y producto
columnas_categoricas = ["cliente", "producto"]
preprocesador = ColumnTransformer([
    ("onehot", OneHotEncoder(handle_unknown='ignore'), columnas_categoricas)
], remainder="passthrough")

# === Pipeline con modelo
pipeline = Pipeline(steps=[
    ("preprocesamiento", preprocesador),
    ("modelo", RandomForestRegressor(random_state=42))
])

# === Búsqueda de hiperparámetros
param_grid = {
    "modelo__n_estimators": [100, 200],
    "modelo__max_depth": [None, 10, 20],
    "modelo__min_samples_split": [2, 5],
}

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar con búsqueda
grid = GridSearchCV(pipeline, param_grid, cv=3, scoring='r2', n_jobs=-1, verbose=1)
grid.fit(X_train, y_train)

# Evaluar
y_pred = grid.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"🎯 Mejor combinación: {grid.best_params_}")
print(f"📉 MSE mejorado: {mse:.2f}")
print(f"📈 R² mejorado: {r2:.4f}")

# Guardar modelo
import joblib
joblib.dump(grid.best_estimator_, "modelo_rf_mejorado.pkl")

# Predicción personalizada
nueva_compra = pd.DataFrame([{
    "cliente": "Eric Aracena",
    "producto": "Delta",
    "cantidad": 30,
    "cliente_freq": cliente_freq.get("Eric Aracena", 0),
    "producto_freq": producto_freq.get("Delta", 0)
}])

monto_estimado = grid.predict(nueva_compra)
print(f"💰 Monto estimado (mejorado): ${monto_estimado[0]:,.2f}")
