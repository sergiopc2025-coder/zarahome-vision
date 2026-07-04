import json
import os
import re
import shutil
import requests

with open("catalogo_final_zarahome.json", "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)

carpeta_base = "catalogo_imagenes_limpio"

if os.path.exists(carpeta_base):
    shutil.rmtree(carpeta_base)

os.makedirs(carpeta_base, exist_ok=True)

total_descargadas = 0
productos_con_fotos = 0
productos_sin_fotos = []

for producto in catalogo:
    referencia = producto.get("referencia", "")
    url_producto = producto.get("url", "")
    imagenes = producto.get("imagenes", [])

    if referencia == "":
        continue

    referencia_limpia = referencia.replace("/", "-")
    carpeta_producto = os.path.join(carpeta_base, referencia_limpia)
    os.makedirs(carpeta_producto, exist_ok=True)

    coincidencia = re.search(r"-l(\d+)", url_producto)
    id_producto = coincidencia.group(1) if coincidencia else ""

    imagenes_filtradas = []

    for img in imagenes:
        if ".jpg" not in img:
            continue

        if id_producto and id_producto in img:
            if img not in imagenes_filtradas:
                imagenes_filtradas.append(img)

    if len(imagenes_filtradas) == 0:
        for img in imagenes:
            if ".jpg" in img and img not in imagenes_filtradas:
                imagenes_filtradas.append(img)

    descargadas_producto = 0

    for numero, url_imagen in enumerate(imagenes_filtradas, start=1):
        try:
            respuesta = requests.get(url_imagen, timeout=20)

            if respuesta.status_code == 200:
                ruta_archivo = os.path.join(carpeta_producto, f"foto_{numero}.jpg")

                with open(ruta_archivo, "wb") as archivo_imagen:
                    archivo_imagen.write(respuesta.content)

                descargadas_producto += 1
                total_descargadas += 1

        except Exception as error:
            print("Error descargando:", url_imagen)
            print(error)

    if descargadas_producto > 0:
        productos_con_fotos += 1
        print("OK:", referencia, "-", descargadas_producto, "fotos")
    else:
        productos_sin_fotos.append(referencia)
        print("SIN FOTOS:", referencia)

print("")
print("Descarga limpia terminada.")
print("Productos con fotos:", productos_con_fotos)
print("Productos sin fotos:", len(productos_sin_fotos))
print("Imágenes descargadas:", total_descargadas)

if productos_sin_fotos:
    print("Referencias sin fotos:")
    for ref in productos_sin_fotos:
        print(ref)