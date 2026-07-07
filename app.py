import base64
import json
import pickle
from textwrap import dedent

import streamlit as st
import torch
import torch.nn.functional as F
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


HEADER_LOGO = "logo.png"
CIRCLE_LOGO = "assets/logo_circulo.png"


st.set_page_config(
    page_title="ZARA HOME VISION",
    page_icon=HEADER_LOGO,
    layout="wide",
)


def html(content):
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)


html("""
<style>
.stApp {
    background: #ffffff;
    color: #111111;
}

.block-container {
    max-width: 1240px;
    padding-top: 18px;
    padding-bottom: 46px;
}

.top-logo-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto 18px auto;
}

.top-logo {
    width: min(980px, 94vw);
    height: auto;
    display: block;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #d9d9d9;
    border-radius: 22px;
    padding: 30px 34px 28px 34px;
    min-height: 520px;
    box-shadow: none;
    background: #ffffff;
}

.section-head {
    display: flex;
    align-items: center;
    gap: 20px;
    padding-bottom: 24px;
    border-bottom: 1px solid #d7d7d7;
    margin-bottom: 24px;
}

.icon-bubble {
    width: 58px;
    height: 58px;
    border-radius: 999px;
    background: #f5eee8;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
}

.section-title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: .2px;
    margin: 0;
}

.helper-text {
    color: #555555;
    font-size: 18px;
    line-height: 1.55;
    margin: 0 0 28px 22px;
    max-width: 410px;
}

.upload-visual {
    border: 2px dashed #d8d8d8;
    border-radius: 18px;
    padding: 30px 22px;
    text-align: center;
    margin-bottom: 18px;
    background: #ffffff;
}

.upload-circle {
    width: 116px;
    height: 116px;
    border-radius: 999px;
    border: 1px solid #d8d8d8;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 14px auto;
    background: #ffffff;
    overflow: hidden;
}

.upload-circle img {
    width: 104px;
    max-width: 104px;
    height: auto;
    display: block;
}

.upload-main {
    font-size: 22px;
    font-weight: 750;
    margin-bottom: 6px;
}

.upload-sub {
    color: #666666;
    font-size: 16px;
}

.empty-result {
    min-height: 245px;
    border-radius: 16px;
    background: #fafafa;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin-top: 96px;
    padding: 28px;
}

.empty-title {
    font-size: 18px;
    font-weight: 750;
    margin-top: 18px;
    margin-bottom: 10px;
}

.empty-text {
    color: #666666;
    font-size: 16px;
}

.product-title {
    font-size: 24px;
    font-weight: 750;
    margin-top: 18px;
}

.label {
    font-size: 13px;
    color: #777777;
    letter-spacing: 1.1px;
    margin-top: 18px;
}

.value {
    font-size: 22px;
    font-weight: 500;
}

.price {
    font-size: 32px;
    font-weight: 500;
}

.stButton > button,
.stLinkButton > a {
    background: #111111 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 13px 22px !important;
    font-size: 16px !important;
    font-weight: 750 !important;
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
    font-weight: 750 !important;
}

@media (max-width: 900px) {
    .block-container {
        padding-top: 12px;
    }

    .top-logo-wrap {
        margin-bottom: 14px;
    }

    .top-logo {
        width: min(760px, 96vw);
    }

    .section-title {
        font-size: 22px;
    }

    .helper-text {
        margin-left: 0;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        min-height: auto;
        padding: 24px 22px;
    }
}
</style>
""")


def asset_data_uri(path):
    try:
        with open(path, "rb") as archivo:
            encoded = base64.b64encode(archivo.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    except Exception:
        return ""


def svg_camera():
    return """
    <svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M14.5 4l1.6 2.4H19a2 2 0 0 1 2 2V18a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8.4a2 2 0 0 1 2-2h2.9L9.5 4h5z"/>
        <circle cx="12" cy="13" r="4"/>
    </svg>
    """


def svg_search():
    return """
    <svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="7"/>
        <path d="M20 20l-4.4-4.4"/>
    </svg>
    """


def svg_bag():
    return """
    <svg viewBox="0 0 24 24" width="34" height="34" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M6 7h12l1 14H5L6 7z"/>
        <path d="M9 7a3 3 0 0 1 6 0"/>
    </svg>
    """


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


header_logo_uri = asset_data_uri(HEADER_LOGO)

if header_logo_uri:
    html(f"""
    <div class="top-logo-wrap">
        <img class="top-logo" src="{header_logo_uri}">
    </div>
    """)
else:
    html("""
    <div style="text-align:center; margin-bottom:18px;">
        <h1 style="font-family:Georgia,serif; font-size:92px; font-weight:400; margin:0;">ZARA HOME</h1>
        <div style="letter-spacing:34px; font-size:28px; margin-left:30px;">VISION</div>
        <div style="width:150px; height:1px; background:#111; margin:22px auto;"></div>
        <div style="letter-spacing:12px; font-size:22px; font-weight:600;">CATALOGO DE PRODUCTOS</div>
        <div style="letter-spacing:10px; font-size:15px; margin-top:14px;">IDENTIFICABLES CON IA</div>
    </div>
    """)


modelo, procesador = cargar_ia()
base_vectores, catalogo = cargar_datos()

if "producto" not in st.session_state:
    st.session_state.producto = None
if "score" not in st.session_state:
    st.session_state.score = None


col1, col2 = st.columns(2, gap="large")

with col1:
    with card_container():
        circle_logo_uri = asset_data_uri(CIRCLE_LOGO) or asset_data_uri(HEADER_LOGO)
        circle_logo_html = f'<img src="{circle_logo_uri}">' if circle_logo_uri else ""

        html(f"""
        <div class="section-head">
            <div class="icon-bubble">{svg_camera()}</div>
            <h2 class="section-title">BUSCA POR IMAGEN</h2>
        </div>

        <p class="helper-text">Sube una foto o usa la camara para identificar un producto.</p>

        <div class="upload-visual">
            <div class="upload-circle">
                {circle_logo_html}
            </div>
            <div class="upload-main">Selecciona una imagen</div>
            <div class="upload-sub">Elige galeria o camara</div>
        </div>
        """)

        opcion = st.selectbox(
            "Selecciona una imagen",
            ["Selecciona una imagen", "Usar una imagen de mi galeria", "Usar la camara"],
            label_visibility="collapsed",
        )

        imagen_fuente = None

        if opcion == "Usar una imagen de mi galeria":
            imagen_fuente = st.file_uploader(
                "Selecciona una imagen",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
            )

        elif opcion == "Usar la camara":
            imagen_fuente = st.camera_input(
                "Haz una foto",
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
        html(f"""
        <div class="section-head">
            <div class="icon-bubble">{svg_search()}</div>
            <h2 class="section-title">PRODUCTO IDENTIFICADO</h2>
        </div>
        """)

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

            html(f'<div class="product-title">{producto["nombre"]}</div>')

            html('<div class="label">REFERENCIA</div>')
            html(f'<div class="value">{producto["referencia"]}</div>')

            html('<div class="label">PRECIO</div>')
            html(f'<div class="price">{producto["precio"]}</div>')

            html('<div class="label">COINCIDENCIA VISUAL</div>')
            st.progress(float(mejor_score))
            html(f'<div class="value">{round(mejor_score * 100, 2)}%</div>')

            st.link_button(
                "VER PRODUCTO EN ZARA HOME",
                producto["url"],
                use_container_width=True,
            )
        else:
            html(f"""
            <div class="empty-result">
                <div>
                    <div class="icon-bubble" style="margin:0 auto;">{svg_bag()}</div>
                    <div class="empty-title">Sube una imagen para empezar.</div>
                    <div class="empty-text">El producto identificado aparecera aqui.</div>
                </div>
            </div>
            """)