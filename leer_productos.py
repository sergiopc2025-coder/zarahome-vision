import json

with open("productos.json", "r", encoding="utf-8") as archivo:
    productos = json.load(archivo)

busqueda = input("¿Qué producto buscas? ")

for producto in productos:
    if busqueda.lower() in producto["nombre"].lower():
        print("")
        print("Producto encontrado:")
        print("Nombre:", producto["nombre"])
        print("Precio:", producto["precio"])
        print("Referencia:", producto["referencia"])