from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/api/minera", methods=["POST"])
def repassar():
    data = request.get_json()
    try:
        response = requests.post("http://192.168.18.25:5000/api/minera", json=data, timeout=90)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": f"Erro no redirecionamento: {str(e)}"})

@app.route("/", methods=["GET"])
def home():
    return "MineraZap Proxy ativo no Railway"
