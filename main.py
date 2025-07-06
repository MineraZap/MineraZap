from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Lê o destino do proxy a partir da variável de ambiente (ou usa um padrão local)
PROXY_TARGET = os.getenv("PROXY_TARGET", "http://127.0.0.1:5000")

@app.route("/api/minera", methods=["POST"])
def repassar():
    data = request.get_json()
    try:
        response = requests.post(f"{PROXY_TARGET}/api/minera", json=data, timeout=90)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": f"Erro no redirecionamento: {str(e)}"})

@app.route("/", methods=["GET"])
def home():
    return "MineraZap Proxy ativo no Railway"

if __name__ == "__main__":
    print(f"🚀 Proxy apontando para: {PROXY_TARGET}")
    app.run(host="0.0.0.0", port=5000, debug=True)
