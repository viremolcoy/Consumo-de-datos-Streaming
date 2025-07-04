from flask import Flask, request, jsonify
import json
import datetime
import pandas as pd
import os

app = Flask(__name__)

# Ruta del archivo CSV
CSV_FILE = "datos_realtime.csv"

# Inicializar el CSV si no existe
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=[
        "id_cliente", "cliente", "genero", "id_producto", "producto",
        "precio", "cantidad", "monto", "forma_pago", "fecreg"
    ])
    df.to_csv(CSV_FILE, index=False)

@app.route('/webhook', methods=['POST'])
def recibir_datos():
    try:
        if request.is_json:
            contenido = request.get_json()

            print(f"\n📩 [{datetime.datetime.now().isoformat()}] Datos recibidos:")

            # Convertimos a DataFrame y guardamos en CSV
            df = pd.DataFrame(contenido)
            df.to_csv(CSV_FILE, mode='a', header=False, index=False)

            print(df)  # Mostrar en consola lo recibido
            return jsonify({"mensaje": "✅ Datos guardados en CSV"}), 200
        else:
            print("❌ El contenido no es JSON válido.")
            print("Recibido:", request.data.decode('utf-8'))
            return jsonify({"error": "Formato no válido"}), 400
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": "Error procesando datos"}), 500

if __name__ == '__main__':
    app.run(port=5000)
