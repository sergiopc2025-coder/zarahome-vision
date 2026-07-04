from playwright.sync_api import sync_playwright
import json
import re

with open("urls_productos.json", "r", encoding="utf-8") as archivo:
    urls = json.load(archivo)

catalogo = []

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()

    for numero, url in enumerate(urls, start=1):
        print(f"Leyendo {numero}/{len(urls)}:", url)

        pagina.goto(url)
        pagina.wait_for_timeout(8000)

        texto = pagina.locator("body").inner_text()
        lineas = [linea.strip() for linea in texto.split("\n") if linea.strip()]

        nombre = ""
        precio = ""
        referencia = ""

        referencias = re.findall(r"\d{4}/\d{3}/\d{3}", texto)
        if referencias:
            referencia = referencias[0]

        for linea in lineas:
            if "Zara Home España" in linea:
                nombre = linea.replace("| Zara Home España", "").strip()
                break

        for linea in lineas:
            if "€" in linea:
                precio = linea
                break

        imagenes = pagina.locator("img").evaluate_all("""
            elementos => elementos
                .map(img => img.src)
                .filter(src => src.includes(".jpg"))
        """)

        imagenes_limpias = []

        for img in imagenes:
            if img not in imagenes_limpias:
                imagenes_limpias.append(img)

        catalogo.append({
            "nombre": nombre,
            "precio": precio,
            "referencia": referencia,
            "url": url,
            "imagenes": imagenes_limpias
        })

    with open("catalogo_final_zarahome.json", "w", encoding="utf-8") as archivo:
        json.dump(catalogo, archivo, indent=2, ensure_ascii=False)

    print("")
    print("Catálogo final creado.")
    print("Productos guardados:", len(catalogo))

    input("Pulsa Enter para cerrar...")
    navegador.close()