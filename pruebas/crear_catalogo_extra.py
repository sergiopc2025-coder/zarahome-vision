from playwright.sync_api import sync_playwright
import json
import re

with open("extras_urls.txt", "r", encoding="utf-8") as archivo:
    urls = [line.strip() for line in archivo if line.strip()]

productos = []

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()

    for i, url in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] Procesando:", url)

        pagina.goto(url)
        pagina.wait_for_timeout(7000)

        texto = pagina.locator("body").inner_text()

        nombre = ""
        precio = ""
        referencia = ""

        for linea in texto.split("\n"):
            if "Zara Home España" in linea:
                nombre = linea.replace("| Zara Home España", "").strip()

            if "€" in linea and precio == "":
                precio = linea.strip()

        refs = re.findall(r"\d{4}/\d{3}/\d{3}", texto)
        if refs:
            referencia = refs[0]

        imagenes = pagina.locator("img").evaluate_all("""
            elementos => elementos
                .map(img => img.src)
                .filter(src => src.includes(".jpg"))
        """)

        imagenes_limpias = []
        for img in imagenes:
            if img not in imagenes_limpias:
                imagenes_limpias.append(img)

        productos.append({
            "nombre": nombre,
            "precio": precio,
            "referencia": referencia,
            "url": url,
            "imagenes": imagenes_limpias
        })

    navegador.close()

with open("catalogo_extra.json", "w", encoding="utf-8") as archivo:
    json.dump(productos, archivo, ensure_ascii=False, indent=4)

print()
print("CATÁLOGO EXTRA CREADO")
print("Productos:", len(productos))