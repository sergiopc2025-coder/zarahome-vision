import json
import os
import requests

with open("catalogo_final_zarahome.json", "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)

carpeta_base = "catalogo_imagenes"
os.makedirs(carpeta_base, exist_ok=True)

total_descargadas = 0

for producto in catalogo:
    referencia = producto.get("referencia", "")

    if referencia == "":
        continue

    carpeta_producto = os.path.join(carpeta_base, referencia.replace("/", "-"))
    os.makedirs(carpeta_producto, exist_ok=True)

    imagenes = producto.get("imagenes", [])

    for numero, url_imagen in enumerate(imagenes, start=1):
        try:
            respuesta = requests.get(url_imagen, timeout=20)

            if respuesta.status_code == 200:
                ruta_archivo = os.path.join(carpeta_producto, f"foto_{numero}.jpg")

                with open(ruta_archivo, "wb") as archivo_imagen:
                    archivo_imagen.write(respuesta.content)

                total_descargadas += 1
                print("Descargada:", ruta_archivo)

        except Exception as error:
            print("Error:", error)

print("Descarga terminada.")
print("Imágenes descargadas:", total_descargadas)