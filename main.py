from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from src.scraper import buscar_oferta

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "mensagem": "MineraZap rodando com sucesso!"})

@app.route("/api/minera", methods=["POST"])
def minera():
    data = request.get_json()
    termo = data.get("termo")

    if not termo:
        return jsonify({"error": "Campo 'termo' é obrigatório"}), 400

    print(f"Iniciando mineração para: {termo}")
    
    try:
        resultado = buscar_oferta(termo)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Webhook recebido:", data)
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
