from flask import Flask, request, jsonify
from src.scraper import buscar_oferta
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente se o arquivo existir
if os.path.exists(".env"):
    load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensagem": "API MineraZap está online!"})

@app.route("/api/minera", methods=["POST"])
def minera():
    try:
        data = request.get_json()

        if not data or "termo" not in data:
            return jsonify({"error": "Campo 'termo' é obrigatório."}), 400

        termo = data["termo"]
        print(f"Iniciando mineração para: {termo}")
        resultado = buscar_oferta(termo)

        return jsonify({"status": 200, "data": resultado})
    
    except Exception as e:
        print(f"Erro interno: {str(e)}")
        return jsonify({"status": 500, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)