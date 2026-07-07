import json
import pickle

import streamlit as st
import torch
import torch.nn.functional as F
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


HEADER_LOGO = "logo.png"
CIRCLE_LOGO = "logo_circulo.png"


st.set_page_config(
    page_title="ZARA HOME VISION",
    page_icon=CIRCLE_LOGO,
    layout="wide",
)


st.markdown("""
<style>
.stApp {
    background: #ffffff;
    color: #111111;
}

.block-container {
    max-width: 1240px;
    padding-top: 8px;
    padding-bottom: 46px;
}

[data-testid="stImage"] {
    display: flex;
    justify-content: center;
}

.logo-arriba {
    margin-bottom: -18px;
}

.logo-arriba img {
    width: min(1040px, 98vw) !important;
    max-width: 1040px !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #d9d9d9;
    border-radius: 22px;
    padding: 30px 34px 28px 34px;
    min-height: 520px;
    background: #ffffff;
}

h2, h3 {
    color: #111111;
}

.stButton > button,
.stLinkButton > a {
    background: #111111 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 13px 22px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

.stButton > button:hover,
.stLinkButton > a:hover {
    background: #333333 !important;
    color: #ffffff !important;
}

[data-testid="stFileUploader"] section {
    border: 1px solid #e0e0e0;
    background: #ffffff;
    border-radius: 12px;
}

[data-testid="stFileUploader"] button {
    background: #111111 !important;
    color: #ffffff !important;
    border-radius: 9px !important;
    border: none !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploader"] small {
    display: none;
}

@media (max-width: 700px) {
    .block-container {
        padding-top: 0px;
    }

    .logo-arriba {
        margin-bottom: -34px;
    }

    .logo-arriba img {
        width: min(1180px, 116vw) !important;
        max-width: none !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 24px 20px 24px 20px;
        min-height: auto;
    }
}
</style>
""", unsafe_allow_html=True)


def card_container():
    try:
        return st.container(border=True)
    except TypeError:
        return st.container()


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


try:
    logo = Image.open(HEADER_LOGO)
    st.markdown('<div class="logo-arriba">', unsafe_allow_html=True)
    st.image(logo, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
except Exception:
    st.markdown("# ZARA HOME VISION")

st.write("")


modelo, procesador = cargar_ia()
base_vectores, catalogo = cargar_datos()

if "producto" not in st.session_state:
    st.session_state.producto = None
if "score" not in st.session_state:
    st.session_state.score = None


col1, col2 = st.columns(2, gap="large")

with col1:
    with card_container():
        icon_col, title_col = st.columns([1, 5])

        with icon_col:
            st.markdown("### 📷")

        with title_col:
            st.markdown("## BÚSQUEDA POR IMAGEN")

        st.divider()

        st.write("Sube una foto o usa la cámara para identificar un producto.")

        upload_box = st.container(border=True)
        with upload_box:
            try:
                circle_logo = Image.open(CIRCLE_LOGO)
                _, logo_col, _ = st.columns([1.35, 1, 1.35])
                with logo_col:
                    st.image(circle_logo, use_container_width=True)
            except Exception:
                st.info("Guarda el logo del círculo como logo_circulo.png junto a app.py")

            st.markdown(
                "<h3 style='text-align:center; margin-bottom:0;'>Selecciona una imagen</h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='text-align:center; color:#666;'>Pulsa abajo para elegir galería o cámara</p>",
                unsafe_allow_html=True,
            )

            imagen_fuente = st.file_uploader(
                "Selecciona una imagen",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
            )

        if imagen_fuente:
            imagen = Image.open(imagen_fuente).convert("RGB")
            st.image(imagen, caption="Imagen seleccionada", use_container_width=True)

            if st.button("IDENTIFICAR PRODUCTO", use_container_width=True):
                with st.spinner("Analizando producto..."):
                    inputs = procesador(images=imagen, return_tensors="pt")

                    with torch.no_grad():
                        salida = modelo.vision_model(**inputs)
                        vector_consulta = salida.pooler_output

                    vector_consulta = F.normalize(vector_consulta, p=2, dim=1)

                    mejor_score = -1
                    mejor_referencia = ""

                    for item in base_vectores:
                        score = torch.matmul(vector_consulta, item["vector"].T).item()

                        if score > mejor_score:
                            mejor_score = score
                            mejor_referencia = item["referencia"]

                    producto = next(
                        (p for p in catalogo if p["referencia"] == mejor_referencia),
                        None,
                    )

                    st.session_state.producto = producto
                    st.session_state.score = mejor_score


with col2:
    with card_container():
        icon_col, title_col = st.columns([1, 5])

        with icon_col:
            st.markdown("### 🔍")

        with title_col:
            st.markdown("## PRODUCTO IDENTIFICADO")

        st.divider()

        producto = st.session_state.producto
        mejor_score = st.session_state.score

        if producto:
            if producto.get("imagenes"):
                st.image(
                    producto["imagenes"][0],
                    caption="Imagen oficial del producto",
                    use_container_width=True,
                )
            else:
                st.info("Imagen oficial no disponible.")

            st.markdown(f"### {producto['nombre']}")

            st.caption("REFERENCIA")
            st.markdown(f"## {producto['referencia']}")

            st.caption("PRECIO")
            st.markdown(f"# {producto['precio']}")

            st.caption("COINCIDENCIA VISUAL")
            st.progress(float(mejor_score))
            st.markdown(f"## {round(mejor_score * 100, 2)}%")

            st.link_button(
                "VER PRODUCTO EN ZARA HOME",
                producto["url"],
                use_container_width=True,
            )
        else:
            st.write("")
            st.write("")
            st.write("")
            empty_box = st.container(border=True)
            with empty_box:
                st.markdown(
                    "<h1 style='text-align:center;'>🛍️</h1>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<h3 style='text-align:center;'>Sube una imagen para empezar.</h3>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<p style='text-align:center; color:#666;'>El producto identificado aparecerá aquí.</p>",
                    unsafe_allow_html=True,
                )