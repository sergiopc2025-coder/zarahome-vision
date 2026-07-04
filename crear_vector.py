from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

print("Cargando CLIP...")

modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("CLIP cargado")

imagen = Image.open("catalogo_imagenes_limpio/0373-046-779/foto_1.jpg")

inputs = procesador(images=imagen, return_tensors="pt")

with torch.no_grad():
    salida = modelo.vision_model(**inputs)
    vector = salida.pooler_output

print("Vector creado correctamente")
print("Tamaño del vector:")
print(vector.shape)

print("Primeros números del vector:")
print(vector[0][:10])