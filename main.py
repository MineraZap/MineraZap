from flask import Flask, request, jsonify
from src.scraper import minerar_termo # Certifique-se de que existe e está funcional

app = Flask(__name__)

@app.route("/", methods=["GET"])
def status():
    return jsonify({"mensagem": "API MineraZap está online."})

@app.route("/minerar", methods=["POST"])
def minerar():
    dados = request.get_json()
    produto = dados.get("produto")

    if not produto:
        return jsonify({"resposta": "Nenhum produto informado."}), 400

    resultado = minerar_termo(produto)

    if isinstance(resultado, str):
        return jsonify({"resposta": resultado})

    resposta_formatada = (
        f"🟢 *Oferta Encontrada*\n"
        f"*Produto:* {resultado['titulo']}\n"
        f"*Anúncios ativos:* {resultado['quantidade']}\n"
        f"*Link:* {resultado['link']}\n"
        f"*Imagem:* {resultado['imagem']}"
    )

    return jsonify({"resposta": resposta_formatada})
