import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from src.scraper import minerar_termo

app = Flask(__name__)
CORS(app)

@app.route("/minerar", methods=["POST"])
def minerar():
    ...

    return jsonify({"mensagem": "API MineraZap está online."})

@app.route('/api/minera', methods=['POST'])
def api_minera():
    data = request.get_json()
    termo = data.get("termo")

    if not termo:
        return jsonify({"error": "Termo de busca não fornecido"}), 400

    try:
        resultado = minerar_termo(termo)
        return jsonify(resultado), 200
    except Exception as e:
        print(f"Erro durante mineração: {str(e)}")
        return jsonify({
            "status": "error",
            "code": 500,
            "message": f"Erro interno: {str(e)}"
        }), 500
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
