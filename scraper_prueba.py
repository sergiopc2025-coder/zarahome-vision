from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()

    pagina.goto("https://www.zarahome.com/es/search.html?term=jarron")
    pagina.wait_for_timeout(3000)

    try:
        pagina.get_by_text("Aceptar todas las cookies").click()
        print("Cookies aceptadas")
    except:
        print("No apareció aviso de cookies")

    print("Página abierta:")
    print(pagina.url)

    input("Pulsa Enter para cerrar...")
    navegador.close()