from playwright.sync_api import sync_playwright
import re

url_producto = "https://www.zarahome.com/es/jarron-decorativo-ceramica-l40376046"

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()

    pagina.goto(url_producto)
    pagina.wait_for_timeout(8000)

    texto = pagina.locator("body").inner_text()

    coincidencias = re.findall(r"\d{4}/\d{3}/\d{3}", texto)

    print("Referencias encontradas:")
    print(coincidencias)

    print("")
    print("Texto donde aparece la referencia:")
    for ref in coincidencias:
        posicion = texto.find(ref)
        print(texto[posicion-80:posicion+120])

    input("Pulsa Enter para cerrar...")
    navegador.close()