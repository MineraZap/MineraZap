from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/api/minera", methods=["POST"])
def minerar():
    data = request.get_json()
    termo = data.get("termo")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=BR&q={termo}&search_type=keyword_unordered"
            page.goto(url)

            page.wait_for_selector('div:has-text("Patrocinado")', timeout=30000)
            cards = page.locator('div:has-text("Patrocinado")').all()

            if not cards:
                return jsonify({
                    "status": "erro",
                    "mensagem": "Nenhum anúncio encontrado para esse termo."
                })

            anuncio = cards[0]
            texto = anuncio.inner_text().split("\n")
            titulo = texto[0] if texto else "Sem texto visível"

            nome_pagina = anuncio.locator('span[class*="xu06os2"]').first.inner_text() if anuncio.locator('span[class*="xu06os2"]').count() > 0 else "Desconhecida"
            imagem = anuncio.locator('img').first.get_attribute('src') if anuncio.locator('img').count() > 0 else "Imagem não encontrada"

            return jsonify({
                "status": "sucesso",
                "termo_recebido": termo,
                "resultado": {
                    "titulo": titulo,
                    "pagina": nome_pagina,
                    "imagem": imagem,
                    "total_ativos": len(cards),
                    "biblioteca": url
                }
            })

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        })

@app.route("/", methods=["GET"])
def home():
    return "API do MineraZap está no ar!"
