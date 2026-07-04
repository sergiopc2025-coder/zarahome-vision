from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()

    pagina.goto("https://www.zarahome.com/es/search.html?term=jarron")
    pagina.wait_for_timeout(7000)

    html = pagina.content()

    with open("zarahome_jarron.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)

    print("HTML guardado en zarahome_jarron.html")

    input("Pulsa Enter para cerrar...")
    navegador.close()