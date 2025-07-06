from flask import Flask, request, jsonify
from src.scraper import minerar_termo  # ajustado para refletir sua estrutura

app = Flask(__name__)

@app.route("/", methods=["GET"])
def status():
    return jsonify({"mensagem": "API MineraZap está online."})

@app.route("/api/minera", methods=["POST"])
def minerar():
    data = request.get_json()
    termo = data.get("termo")

    if not termo:
        return jsonify({"erro": "Campo 'termo' é obrigatório"}), 400

    resultado = minerar_termo(termo)
    return jsonify(resultado)
