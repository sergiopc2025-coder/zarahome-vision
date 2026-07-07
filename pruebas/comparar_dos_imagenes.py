from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import torch.nn.functional as F

print("Cargando CLIP...")

modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("CLIP cargado")

imagen1 = Image.open("catalogo_imagenes_limpio/0373-046-779/foto_1.jpg")
imagen2 = Image.open("catalogo_imagenes_limpio/0373-046-779/foto_2.jpg")

inputs1 = procesador(images=imagen1, return_tensors="pt")
inputs2 = procesador(images=imagen2, return_tensors="pt")

with torch.no_grad():
    salida1 = modelo.vision_model(**inputs1)
    salida2 = modelo.vision_model(**inputs2)

    vector1 = salida1.pooler_output
    vector2 = salida2.pooler_output

vector1 = F.normalize(vector1, p=2, dim=1)
vector2 = F.normalize(vector2, p=2, dim=1)

similitud = torch.matmul(vector1, vector2.T)

print("")
print("Similitud:")
print(similitud.item())