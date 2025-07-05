import os
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Adiciona a pasta 'src' no caminho de importação
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importa função do scraper
from scraper import buscar_oferta

# Carrega variáveis de ambiente se existir .env
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

        # Chamada real ao scraper
        resultado = buscar_oferta(termo)

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
