from transformers import CLIPProcessor, CLIPModel

print("Cargando CLIP...")

modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("CLIP cargado correctamente")