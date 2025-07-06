from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

app = Flask(__name__)

@app.route("/api/minera", methods=["POST"])
def minerar():
    data = request.get_json()
    termo = data.get("termo")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, timeout=8000)
            page = browser.new_page()

            url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=BR&q={termo}&search_type=keyword_unordered"
            page.goto(url, timeout=8000)

            try:
                page.wait_for_selector('div:has-text("Patrocinado")', timeout=8000)
            except PlaywrightTimeout:
                return jsonify({
                    "status": "erro",
                    "mensagem": "Tempo excedido para carregar anúncios. Tente novamente."
                })

            cards = page.locator('div:has-text("Patrocinado")').all()
            if not cards:
                return jsonify({
                    "status": "erro",
                    "mensagem": "Nenhum anúncio encontrado para esse termo."
                })

            anuncio = cards[0]
            linhas = anuncio.inner_text().split("\n")
            titulo = linhas[0] if linhas else "Sem texto visível"

            try:
                imagem = anuncio.locator("img").first.get_attribute("src")
            except:
                imagem = "Não encontrado"

            try:
                pagina = anuncio.locator('span:below(img)').first.inner_text()
            except:
                pagina = "Não identificado"

            return jsonify({
                "status": "sucesso",
                "termo_recebido": termo,
                "resultado": {
                    "titulo": titulo,
                    "pagina": pagina,
                    "imagem": imagem,
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
