from playwright.sync_api import sync_playwright

def minerar_termo(termo):
    print(f"Iniciando mineração para: {termo}")
    url = f"https://www.facebook.com/ads/library/?q={termo}&ad_type=all&country=BR"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        try:
            page.wait_for_selector('div[class*="x1n2onr6"]', timeout=30000)
            cards = page.locator('div[class*="x1n2onr6"]').all()

            if not cards:
                return [{"mensagem": "Nenhum anúncio encontrado"}]

            anuncio = cards[0]
            titulo = anuncio.inner_text().split("\n")[0] if anuncio.inner_text() else "Título não encontrado"

            try:
                nome_pagina = anuncio.locator('span[class*="xu06os2"]').first.inner_text()
            except:
                nome_pagina = "Página não identificada"

            try:
                imagem = anuncio.locator('img').first.get_attribute("src")
            except:
                imagem = "Imagem não encontrada"

            resultado = [{
                "produto": termo,
                "oferta": titulo,
                "pagina": nome_pagina,
                "imagem": imagem,
                "link": url,
                "quantidade_anuncios": len(cards)
            }]
            return resultado

        except Exception as e:
            print(f"Erro durante scraping: {str(e)}")
            return [{"mensagem": f"Erro ao minerar: {str(e)}"}]
        finally:
            browser.close()
