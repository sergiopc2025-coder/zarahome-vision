from playwright.sync_api import sync_playwright
import json

categorias = [
    "jarron",
    "lampara",
    "cojin",
    "marco",
    "manta"
]

catalogo = []

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()

    for categoria in categorias:
        url = f"https://www.zarahome.com/es/search.html?term={categoria}"

        print("Buscando:", categoria)

        pagina.goto(url)
        pagina.wait_for_timeout(7000)

        textos = pagina.locator("body").inner_text()
        lineas = textos.split("\n")

        productos_texto = []

        for i in range(len(lineas) - 1):
            nombre = lineas[i].strip()
            precio = lineas[i + 1].strip()

            if "€" in precio and len(nombre) > 5:
                productos_texto.append({
                    "nombre": nombre,
                    "precio": precio
                })

        enlaces = pagina.locator("a").evaluate_all("""
            elementos => elementos.map(a => ({
                texto: a.innerText,
                url: a.href
            }))
        """)

        imagenes = pagina.locator("img").evaluate_all("""
            elementos => elementos.map(img => ({
                alt: img.alt,
                src: img.src
            }))
        """)

        for producto in productos_texto:
            nombre = producto["nombre"]

            url_producto = ""
            imagen_producto = ""

            for enlace in enlaces:
                if nombre.upper() in enlace["texto"].upper():
                    url_producto = enlace["url"]
                    break

            for imagen in imagenes:
                if nombre.upper() in imagen["alt"].upper():
                    imagen_producto = imagen["src"]
                    break

            catalogo.append({
                "categoria_busqueda": categoria,
                "nombre": nombre,
                "precio": producto["precio"],
                "url": url_producto,
                "imagen": imagen_producto
            })

    with open("catalogo_zarahome_completo.json", "w", encoding="utf-8") as archivo:
        json.dump(catalogo, archivo, indent=2, ensure_ascii=False)

    print("Productos guardados:", len(catalogo))

    input("Pulsa Enter para cerrar...")
    navegador.close()