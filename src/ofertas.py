from flask import Blueprint, request, jsonify
from src.scraper import minerar_termo

ofertas_bp = Blueprint('ofertas', __name__)

@ofertas_bp.route('/ofertas/ping')
def ping():
    return 'pong'

@ofertas_bp.route('/minera', methods=['POST'])
def minerar_ofertas():
    data = request.get_json()
    termo = data.get('termo', '')

    resultados = minerar_termo(termo)

    return jsonify(resultados)
