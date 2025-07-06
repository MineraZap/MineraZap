from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API do MineraZap está online!"

@app.route("/api/minera", methods=["POST"])
def minera():
    data = request.get_json()
    termo = data.get("termo")

    if not termo:
        return jsonify({"erro": "O campo 'termo' é obrigatório"}), 400

    # Aqui entraria a lógica de mineração com o Playwright, etc.
    # Neste exemplo, está apenas simulando a resposta
    return jsonify({
        "status": "sucesso",
        "termo_recebido": termo,
        "resultados": ["Exemplo 1", "Exemplo 2"]
    })
