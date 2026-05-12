import streamlit as st
import tempfile

from ui.styles import carregar_css
from ui.preview import mostrar_preview
from ui.results import mostrar_resultados

from core.svg_parser import extrair_poligonos_svg
from core.nesting import nesting
from core.metrics import calcular_metricas

from render.canvas import desenhar_layout

st.set_page_config(page_title="ARVO 8.0", layout="wide")

carregar_css()

st.title("ARVO 8.0 - Smart SVG Nesting")

largura_tecido = st.number_input(
    "Largura do tecido",
    min_value=50,
    value=140
)

altura_tecido = st.number_input(
    "Altura do tecido",
    min_value=50,
    value=100
)

quantidade = st.number_input(
    "Quantidade de repetições",
    min_value=1,
    value=2
)

margem = st.number_input(
    "Margem de segurança",
    min_value=0.0,
    value=2.0
)

escala_svg = st.slider(
    "Escala SVG",
    0.1,
    2.0,
    0.35,
    0.05
)

svg_files = st.file_uploader(
    "Upload SVG",
    type=["svg"],
    accept_multiple_files=True
)

if svg_files:
    mostrar_preview(svg_files)

if st.button("Gerar Layout"):

    polys = []

    for arquivo in svg_files:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".svg"
        ) as tmp:

            tmp.write(arquivo.read())

            caminho = tmp.name

        polygons = extrair_poligonos_svg(
            caminho,
            escala_svg
        )

        for poly in polygons:

            for _ in range(quantidade):

                polys.append({
                    "nome": arquivo.name.replace(".svg",""),
                    "poly": poly
                })

    colocadas, sobras = nesting(
        polys,
        largura_tecido,
        altura_tecido,
        margem
    )

    fig = desenhar_layout(
        colocadas,
        largura_tecido,
        altura_tecido
    )

    st.pyplot(fig)

    dados = calcular_metricas(
        colocadas,
        largura_tecido,
        altura_tecido
    )

    mostrar_resultados(
        dados,
        colocadas,
        sobras
    )