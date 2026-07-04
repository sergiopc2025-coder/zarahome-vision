import os

carpeta_base = "catalogo_imagenes"

vacias = 0
con_fotos = 0

for carpeta in os.listdir(carpeta_base):
    ruta = os.path.join(carpeta_base, carpeta)

    if os.path.isdir(ruta):
        fotos = [f for f in os.listdir(ruta) if f.endswith(".jpg")]

        if len(fotos) == 0:
            vacias += 1
            print("Vacía:", carpeta)
        else:
            con_fotos += 1

print("")
print("Carpetas con fotos:", con_fotos)
print("Carpetas vacías:", vacias)