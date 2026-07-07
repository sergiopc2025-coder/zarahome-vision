import json

REFERENCIAS_ELIMINAR = [
    "3121/004/500",
    "6369/004/104",
    "6368/004/518"
]

with open("catalogo_final_zarahome.json", "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)

catalogo_limpio = [
    producto
    for producto in catalogo
    if producto.get("referencia") not in REFERENCIAS_ELIMINAR
]

with open("catalogo_final_zarahome.json", "w", encoding="utf-8") as archivo:
    json.dump(catalogo_limpio, archivo, indent=2, ensure_ascii=False)

print("Productos originales:", len(catalogo))
print("Productos finales:", len(catalogo_limpio))
print("Eliminados:", len(catalogo) - len(catalogo_limpio))