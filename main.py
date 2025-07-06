from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/minera", methods=["POST"])
def minerar():
    termo = request.json.get("termo")
    return jsonify({
        "status": "ok",
        "termo_recebido": termo
    })
