import json
import os
import requests

with open("catalogo_extra.json", "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)

carpeta_base = "catalogo_imagenes_extra"
os.makedirs(carpeta_base, exist_ok=True)

total_descargadas = 0

for producto in catalogo:
    referencia = producto.get("referencia", "")

    if referencia == "":
        continue

    carpeta_producto = referencia.replace("/", "-")
    ruta_carpeta = os.path.join(carpeta_base, carpeta_producto)

    os.makedirs(ruta_carpeta, exist_ok=True)

    imagenes = producto.get("imagenes", [])

    for i, url in enumerate(imagenes, start=1):
        try:
            respuesta = requests.get(url, timeout=20)

            if respuesta.status_code == 200:
                ruta_imagen = os.path.join(ruta_carpeta, f"foto_{i}.jpg")

                with open(ruta_imagen, "wb") as archivo_imagen:
                    archivo_imagen.write(respuesta.content)

                total_descargadas += 1
                print("Descargada:", ruta_imagen)

        except Exception as e:
            print("Error descargando:", url)
            print(e)

print()
print("DESCARGA EXTRA TERMINADA")
print("Imágenes descargadas:", total_descargadas)