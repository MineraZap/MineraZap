from flask import Flask, request, jsonify
from flask_cors import CORS
from src.scraper import buscar_oferta
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Minera Zap rodando com sucesso!"

@app.route('/api/minera', methods=['POST'])
def minera():
    data = request.get_json()
    termo = data.get('termo')

    try:
        resultado = buscar_oferta(termo)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


    try:
        print(f"Iniciando mineração para: {termo}")
        resultado = buscar_oferta(termo)

        return jsonify({"status": "sucesso", "resultado": resultado})
    except Exception as e:
        print(f"Erro na mineração: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
import subprocess
subprocess.run(["playwright", "install", "chromium"])

