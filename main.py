import os
from flask import Flask, request, jsonify
from src.scraper import minerar_anuncios

app = Flask(__name__)

@app.route("/api/minera", methods=["POST"])
def minera():
    data = request.get_json()
    termo = data.get("termo")
    if not termo:
        return jsonify({"erro": "Campo \"termo\" é obrigatório"}), 400
    
    print(f"📨 Recebida requisição para minerar: {termo}")
    resultado = minerar_anuncios(termo)
    return jsonify(resultado)

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "online",
        "servico": "MineraZap API",
        "versao": "1.0.0",
        "endpoints": [
            "POST /api/minera - Minera anúncios do Facebook",
            "GET /api/status - Status da API"
        ]
    })

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "mensagem": "MineraZap API está funcionando!",
        "uso": "POST /api/minera com JSON {\"termo\": \"sua_palavra_chave\"}",
        "exemplo": "curl -X POST http://localhost:7010/api/minera -H \"Content-Type: application/json\" -d \"{\\\"termo\\\":\\\"relógio inteligente\\\"}\""
    } )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7010)) # Usa a porta do ambiente ou 7010 como fallback
    print(f"🚀 Iniciando MineraZap API na porta {port}...")
    print(f"📍 Acesse: http://localhost:{port}" )
    print(f"🔧 Teste: curl -X POST http://localhost:{port}/api/minera -H \"Content-Type: application/json\" -d \"{{\\\"termo\\\":\\\"relógio\\\"}}\"" )
    app.run(host="0.0.0.0", port=port)
