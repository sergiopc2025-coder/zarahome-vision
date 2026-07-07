from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import torch.nn.functional as F
import os
import pickle

print("Cargando CLIP...")

modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("CLIP cargado")

base_vectores = []

carpeta_base = "catalogo_imagenes_limpio"

total = 0

for referencia in os.listdir(carpeta_base):
    ruta_referencia = os.path.join(carpeta_base, referencia)

    if not os.path.isdir(ruta_referencia):
        continue

    for archivo in os.listdir(ruta_referencia):
        if not archivo.lower().endswith(".jpg"):
            continue

        ruta_imagen = os.path.join(ruta_referencia, archivo)

        try:
            imagen = Image.open(ruta_imagen).convert("RGB")
            inputs = procesador(images=imagen, return_tensors="pt")

            with torch.no_grad():
                salida = modelo.vision_model(**inputs)
                vector = salida.pooler_output

            vector = F.normalize(vector, p=2, dim=1)

            base_vectores.append({
                "referencia": referencia.replace("-", "/"),
                "ruta": ruta_imagen,
                "vector": vector
            })

            total += 1
            print("Vector creado:", total, ruta_imagen)

        except Exception as error:
            print("Error con:", ruta_imagen)
            print(error)

with open("base_vectores.pkl", "wb") as archivo:
    pickle.dump(base_vectores, archivo)

print("")
print("Base de vectores creada.")
print("Vectores guardados:", len(base_vectores))