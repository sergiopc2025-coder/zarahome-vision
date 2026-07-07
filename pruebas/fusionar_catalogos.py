import json
import os
import shutil

with open("catalogo_final_zarahome.json", "r", encoding="utf-8") as archivo:
    catalogo_principal = json.load(archivo)

with open("catalogo_extra.json", "r", encoding="utf-8") as archivo:
    catalogo_extra = json.load(archivo)

referencias_existentes = {
    producto["referencia"]
    for producto in catalogo_principal
}

nuevos = []

for producto in catalogo_extra:
    referencia = producto.get("referencia", "")

    if referencia and referencia not in referencias_existentes:
        nuevos.append(producto)
        referencias_existentes.add(referencia)

catalogo_fusionado = catalogo_principal + nuevos

with open("catalogo_final_zarahome.json", "w", encoding="utf-8") as archivo:
    json.dump(catalogo_fusionado, archivo, indent=4, ensure_ascii=False)

origen = "catalogo_imagenes_extra"
destino = "catalogo_imagenes_limpio"

copiadas = 0

for carpeta in os.listdir(origen):
    ruta_origen = os.path.join(origen, carpeta)
    ruta_destino = os.path.join(destino, carpeta)

    if os.path.isdir(ruta_origen):
        if not os.path.exists(ruta_destino):
            shutil.copytree(ruta_origen, ruta_destino)
            copiadas += 1

print("Productos principales:", len(catalogo_principal))
print("Productos extra:", len(catalogo_extra))
print("Productos nuevos añadidos:", len(nuevos))
print("Total final:", len(catalogo_fusionado))
print("Carpetas de imágenes copiadas:", copiadas)