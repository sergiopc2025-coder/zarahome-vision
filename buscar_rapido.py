from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import torch.nn.functional as F
import pickle
import json
import os

print("Cargando CLIP...")

modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("CLIP cargado")

with open("base_vectores.pkl", "rb") as archivo:
    base_vectores = pickle.load(archivo)

with open("catalogo_final_zarahome.json", "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)

consulta = "fotos_prueba/prueba1.jpg"

imagen = Image.open(consulta).convert("RGB")
inputs = procesador(images=imagen, return_tensors="pt")

with torch.no_grad():
    salida = modelo.vision_model(**inputs)
    vector_consulta = salida.pooler_output

vector_consulta = F.normalize(vector_consulta, p=2, dim=1)

mejores = []

for item in base_vectores:
    if os.path.normpath(item["ruta"]) == os.path.normpath(consulta):
        continue

    score = torch.matmul(vector_consulta, item["vector"].T).item()

    mejores.append({
        "referencia": item["referencia"],
        "ruta": item["ruta"],
        "score": score
    })

mejores = sorted(mejores, key=lambda x: x["score"], reverse=True)

print("")
print("TOP 5 RESULTADOS")
print("----------------")

for resultado in mejores[:5]:
    producto = next(
        (p for p in catalogo if p["referencia"] == resultado["referencia"]),
        None
    )

    if producto:
        print("")
        print("Nombre:", producto["nombre"])
        print("Referencia:", producto["referencia"])
        print("Precio:", producto["precio"])
        print("Score:", resultado["score"])
        print("Imagen:", resultado["ruta"])
        print("URL:", producto["url"])