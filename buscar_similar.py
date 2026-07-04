from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import torch.nn.functional as F
import os

print("Cargando CLIP...")

modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("CLIP cargado")

consulta = "catalogo_imagenes_limpio/0373-046-779/foto_2.jpg"

imagen_consulta = Image.open(consulta)
inputs = procesador(images=imagen_consulta, return_tensors="pt")

with torch.no_grad():
    salida = modelo.vision_model(**inputs)
    vector_consulta = salida.pooler_output

vector_consulta = F.normalize(vector_consulta, p=2, dim=1)

mejor_score = -1
mejor_imagen = ""
contador = 0

for carpeta in os.listdir("catalogo_imagenes_limpio"):
    ruta_carpeta = os.path.join("catalogo_imagenes_limpio", carpeta)

    if not os.path.isdir(ruta_carpeta):
        continue

    for archivo in os.listdir(ruta_carpeta):
        if not archivo.endswith(".jpg"):
            continue

        ruta_imagen = os.path.join(ruta_carpeta, archivo)

        if os.path.normpath(ruta_imagen) == os.path.normpath(consulta):
            continue

        contador += 1

        try:
            imagen = Image.open(ruta_imagen)
            inputs = procesador(images=imagen, return_tensors="pt")

            with torch.no_grad():
                salida = modelo.vision_model(**inputs)
                vector = salida.pooler_output

            vector = F.normalize(vector, p=2, dim=1)

            score = torch.matmul(vector_consulta, vector.T).item()

            if score > mejor_score:
                mejor_score = score
                mejor_imagen = ruta_imagen

        except:
            pass

print("")
print("Imágenes comparadas:", contador)
print("Imagen de consulta:")
print(consulta)
print("Mejor coincidencia:")
print(mejor_imagen)
print("Score:")
print(mejor_score)