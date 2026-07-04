from transformers import CLIPProcessor, CLIPModel
from PIL import Image

print("Cargando CLIP...")

modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("CLIP cargado")

imagen = Image.open("catalogo_imagenes_limpio/0373-046-779/foto_1.jpg")

inputs = procesador(images=imagen, return_tensors="pt")

print("Imagen procesada correctamente")
print(inputs["pixel_values"].shape)