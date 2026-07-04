from playwright.sync_api import sync_playwright
import json
import re

categorias = ["jarron", "lampara", "cojin", "marco", "manta"]

urls = []

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()

    for categoria in categorias:
        print("Buscando:", categoria)

        pagina.goto(f"https://www.zarahome.com/es/search.html?term={categoria}")
        pagina.wait_for_timeout(7000)

        enlaces = pagina.locator("a").evaluate_all("""
            elementos => elementos.map(a => a.href)
        """)

        for enlace in enlaces:
            if re.search(r"-l\d+", enlace) and enlace not in urls:
                urls.append(enlace)

    with open("urls_productos.json", "w", encoding="utf-8") as archivo:
        json.dump(urls, archivo, indent=2, ensure_ascii=False)

    print("URLs de producto guardadas:", len(urls))

    input("Pulsa Enter para cerrar...")
    navegador.close()