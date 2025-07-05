from flask import Flask, request, jsonify
from src.user import user_bp
from src.ofertas import ofertas_bp
# from src.scraper import minerar_produto  # deixa comentado por enquanto se estiver dando erro

import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"mensagem": "API MineraZap rodando com sucesso!"})

@app.route("/api/minera", methods=["POST"])
def minerar():
    data = request.get_json()
    termo = data.get("termo")

    if not termo:
        return jsonify({"error": "Parâmetro 'termo' é obrigatório."}), 400

    print(f"Iniciando mineração para: {termo}")

    # resultado = minerar_produto(termo)  # substituir depois quando estiver pronto
    # return jsonify(resultado), 200

    # Temporário só para teste e evitar erro 500:
    return jsonify({"mensagem": f"Busca por '{termo}' recebida com sucesso"}), 200

# Registro dos blueprints
app.register_blueprint(user_bp, url_prefix="/api/user")
app.register_blueprint(ofertas_bp, url_prefix="/api/ofertas")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
