from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

# Importa a função de mineração
from src.scraper import buscar_oferta

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"mensagem": "API do MineraZap rodando com sucesso!"})

@app.route("/api/minera", methods=["POST"])
def minera():
    try:
        data = request.get_json()
        termo = data.get("termo", "")

        if not termo:
            return jsonify({"erro": "Campo 'termo' é obrigatório"}), 400

        print(f"Iniciando mineração para: {termo}")
        resultado = buscar_oferta(termo)

        return jsonify({"status": "sucesso", "resultado": resultado}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
