from playwright.sync_api import sync_playwright

def minerar_termo(termo):
    print(f"🔍 Iniciando mineração para: {termo}")
    url = f"https://www.facebook.com/ads/library/?q={termo}&ad_type=all&country=BR"
    print(f"🌐 URL de busca: {url}")

    with sync_playwright() as p:
        print("🚀 Iniciando navegador headless...")
        browser = p.chromium.launch(headless=False, args=["--no-sandbox"])

        context = browser.new_context()
        page = context.new_page()

        print("📥 Acessando página...")
        page.goto(url)

        try:
            print("⏳ Esperando aparecer os cards de anúncio...")
            page.wait_for_selector('div[class*="x1n2onr6"]', timeout=30000)
            cards = page.locator('div[class*="x1n2onr6"]').all()
            print(f"🔎 {len(cards)} cards encontrados.")

            if not cards:
                print("⚠️ Nenhum anúncio encontrado.")
                return [{"mensagem": "Nenhum anúncio encontrado"}]

            anuncio = cards[0]
            texto_anuncio = anuncio.inner_text()
            print(f"📝 Texto capturado do primeiro anúncio: {texto_anuncio[:100]}...")

            titulo = texto_anuncio.split("\n")[0] if texto_anuncio else "Título não encontrado"

            try:
                nome_pagina = anuncio.locator('span[class*="xu06os2"]').first.inner_text()
                print(f"🏷 Nome da página: {nome_pagina}")
            except:
                nome_pagina = "Página não identificada"
                print("⚠️ Nome da página não encontrado.")

            try:
                imagem = anuncio.locator('img').first.get_attribute("src")
                print(f"🖼 Imagem: {imagem}")
            except:
                imagem = "Imagem não encontrada"
                print("⚠️ Imagem não encontrada.")

            resultado = [{
                "produto": termo,
                "oferta": titulo,
                "pagina": nome_pagina,
                "imagem": imagem,
                "link": url,
                "quantidade_anuncios": len(cards)
            }]

            print("✅ Mineração finalizada com sucesso.")
            return resultado

        except Exception as e:
            print(f"❌ Erro durante scraping: {str(e)}")
            return [{"mensagem": f"Erro ao minerar: {str(e)}"}]
        finally:
            print("🧹 Encerrando navegador.")
            browser.close()
