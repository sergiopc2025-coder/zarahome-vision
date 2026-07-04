import streamlit as st
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
import torch.nn.functional as F
import pickle
import json

st.set_page_config(
    page_title="ZARA HOME VISION",
    page_icon="🏺",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: #f7f2eb;
    color: #111;
}

.block-container {
    max-width: 1100px;
    padding-top: 35px;
}

.logo {
    text-align: center;
    font-size: 72px;
    font-weight: 700;
    letter-spacing: 5px;
    color: #111;
    margin-bottom: -12px;
}

.vision {
    text-align: center;
    font-size: 26px;
    letter-spacing: 16px;
    color: #a99070;
    margin-bottom: 40px;
}

.card-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 20px;
}

.label {
    font-size: 13px;
    color: #777;
    letter-spacing: 1px;
    margin-top: 18px;
}

.value {
    font-size: 24px;
    font-weight: 500;
    color: #111;
}

.price {
    font-size: 34px;
    font-weight: 500;
    color: #111;
}

.stButton > button {
    background: #111;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 14px 20px;
    font-size: 16px;
    width: 100%;
}

.stButton > button:hover {
    background: #333;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo">ZARA HOME</div>', unsafe_allow_html=True)
st.markdown('<div class="vision">VISION</div>', unsafe_allow_html=True)

@st.cache_resource
def cargar_ia():
    modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return modelo, procesador

@st.cache_data
def cargar_datos():
    with open("base_vectores.pkl", "rb") as archivo:
        base_vectores = pickle.load(archivo)

    with open("catalogo_final_zarahome.json", "r", encoding="utf-8") as archivo:
        catalogo = json.load(archivo)

    return base_vectores, catalogo

modelo, procesador = cargar_ia()
base_vectores, catalogo = cargar_datos()

col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown("### BUSCA POR IMAGEN")
    st.write("Sube una foto o usa la cámara para identificar un producto.")

    archivo = st.file_uploader(
        "📷 Selecciona una imagen",
        type=["jpg", "jpeg", "png"]
    )

    if archivo:
        imagen = Image.open(archivo).convert("RGB")
        st.image(imagen, caption="Foto subida", use_container_width=True)

with col2:
    st.markdown("### PRODUCTO IDENTIFICADO")

    if archivo:
        if st.button("🔍 IDENTIFICAR PRODUCTO"):
            with st.spinner("Analizando producto..."):
                inputs = procesador(images=imagen, return_tensors="pt")

                with torch.no_grad():
                    salida = modelo.vision_model(**inputs)
                    vector_consulta = salida.pooler_output

                vector_consulta = F.normalize(vector_consulta, p=2, dim=1)

                mejor_score = -1
                mejor_referencia = ""
                mejor_imagen = ""

                for item in base_vectores:
                    score = torch.matmul(
                        vector_consulta,
                        item["vector"].T
                    ).item()

                    if score > mejor_score:
                        mejor_score = score
                        mejor_referencia = item["referencia"]
                        mejor_imagen = item["ruta"]

                producto = next(
                    (p for p in catalogo if p["referencia"] == mejor_referencia),
                    None
                )

            if producto:
                try:
                    st.image(
                        mejor_imagen,
                        caption="Imagen oficial más parecida",
                        use_container_width=True
                    )
                except:
                    st.info("Imagen oficial no disponible en la versión online.")

                st.markdown(f'<div class="card-title">{producto["nombre"]}</div>', unsafe_allow_html=True)

                st.markdown('<div class="label">REFERENCIA</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="value">{producto["referencia"]}</div>', unsafe_allow_html=True)

                st.markdown('<div class="label">PRECIO</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="price">{producto["precio"]}</div>', unsafe_allow_html=True)

                st.markdown('<div class="label">COINCIDENCIA VISUAL</div>', unsafe_allow_html=True)
                st.progress(float(mejor_score))
                st.markdown(f'<div class="value">{round(mejor_score * 100, 2)}%</div>', unsafe_allow_html=True)

                st.link_button(
                    "VER PRODUCTO EN ZARA HOME",
                    producto["url"],
                    use_container_width=True
                )
    else:
        st.info("Sube una imagen para empezar.")