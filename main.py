from flask import Flask, request, jsonify
from src.scraper import minerar_termo
import re

app = Flask(__name__)

@app.route("/api/minera", methods=["POST"])
def minerar():
    data = request.get_json()
    termo = data.get("termo", "").strip()

    if not termo:
        return jsonify({"mensagem": "Erro: nenhum termo fornecido."})

    print(f"Iniciando busca pelo termo: {termo}")
    resultado = minerar_termo(termo)

    if not resultado:
        return jsonify([{"mensagem": "Nenhum anúncio encontrado"}])

    resposta = {
        "reply": f"""🔥 Oferta escalada encontrada!

🔗 Biblioteca: {resultado[0].get('link', 'Link não disponível')}
📊 Anúncios ativos: {len(resultado)}
📄 Página: {resultado[0].get('pagina', 'Página não identificada')}
🖼️ Criativo mais escalado: {resultado[0].get('imagem', 'Imagem indisponível')}"""
    }

    return jsonify(resposta)


@app.route("/webhook", methods=["POST"])
def responder():
    data = request.get_json()
    mensagem = data.get("mensagem", "").strip().lower()

    match = re.match(r"mineir(?:ar|e)?\s+(.+)", mensagem)
    if match:
        termo = match.group(1).strip()
        print(f"Iniciando mineração para: {termo}")
        resultado = minerar_termo(termo)

        if not resultado:
            return jsonify({"reply": f"Nenhum anúncio encontrado para o termo: {termo}"})

        resposta = f"""🔥 Oferta escalada encontrada para “{termo}”:

🔗 Biblioteca: {resultado[0].get('link', 'Link não disponível')}
📊 Anúncios ativos: {len(resultado)}
📄 Página: {resultado[0].get('pagina', 'Página não identificada')}
🖼️ Criativo mais escalado: {resultado[0].get('imagem', 'Imagem indisponível')}"""

        return jsonify({"reply": resposta})
    else:
        return jsonify({"reply": "Formato inválido. Envie algo como: mineire smartwatch ou mineirar bermuda."})


if __name__ == "__main__":
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "MineraZap está online!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
