from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()

    pagina.goto("https://www.zarahome.com/es/search.html?term=jarron")
    pagina.wait_for_timeout(7000)

    imagenes = pagina.locator("img").evaluate_all("""
        elementos => elementos.map(img => ({
            alt: img.alt,
            src: img.src
        }))
    """)

    productos = []

    for imagen in imagenes:
        alt = imagen["alt"].strip()
        src = imagen["src"]

        if "JARRÓN" in alt.upper():
            productos.append({
                "nombre": alt,
                "imagen": src
            })

    with open("productos_con_imagenes.json", "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, indent=2, ensure_ascii=False)

    print("Productos con imagen guardados:", len(productos))

    input("Pulsa Enter para cerrar...")
    navegador.close()