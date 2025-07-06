from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

app = Flask(__name__)

@app.route("/api/minera", methods=["POST"])
def minerar():
    data = request.get_json()
    termo = data.get("termo", "")

    if not termo:
        return jsonify({"status": "erro", "mensagem": "Termo não informado."}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            context.set_default_timeout(15000)
            page = context.new_page()

            url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=BR&q={termo}&search_type=keyword_unordered"
            page.goto(url)

            page.wait_for_selector('div:has-text("Patrocinado")', timeout=15000)
            cards = page.locator('div:has-text("Patrocinado")').all()

            if not cards:
                return jsonify({"status": "erro", "mensagem": "Nenhum anúncio encontrado."})

            resultados = []

            for card in cards[:10]:
                try:
                    texto_bruto = card.inner_text()
                    linhas = texto_bruto.split("\n")
                    nome_produto = linhas[0] if linhas else "Sem título"
                    nome_pagina = card.locator('span[class*="xu06os2"]').first.inner_text()
                    link_biblioteca = page.url
                    link_criativo = card.locator('img').first.get_attribute("src")

                    resultados.append({
                        "Nome do produto": nome_produto,
                        "Nome da página": nome_pagina,
                        "Link da biblioteca": link_biblioteca,
                        "Link do Criativo": link_criativo,
                    })
                except Exception as e:
                    continue

            if not resultados:
                return jsonify({"status": "erro", "mensagem": "Falha ao extrair dados dos anúncios."})

            return jsonify({
                "status": "sucesso",
                "termo_recebido": termo,
                "quantidade_resultados": len(resultados),
                "resultados": resultados
            })

    except PlaywrightTimeout:
        return jsonify({"status": "erro", "mensagem": "Tempo excedido para carregar anúncios. Tente novamente."})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})

@app.route("/", methods=["GET"])
def home():
    return "API do MineraZap está online!"
