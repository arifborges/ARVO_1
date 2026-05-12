
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon
from shapely.affinity import translate, rotate, scale
from shapely.ops import unary_union
from svgpathtools import svg2paths
from collections import Counter
import numpy as np
import tempfile
import random

st.set_page_config(page_title="ARVO 8.0", layout="wide")

st.markdown("""
<style>
.stApp{
background:#000;
color:white;
}

h1,h2,h3,p,label{
color:white!important;
}

div[data-baseweb="input"] > div{
background:#1a1a1a;
border:1px solid #ff69c9;
border-radius:10px;
}

.stButton>button{
background:linear-gradient(135deg,#ff69c9,#1a1a1a);
color:white;
border:1px solid #ff69c9;
border-radius:12px;
padding:12px 24px;
font-size:16px;
}
</style>
""", unsafe_allow_html=True)

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
    "Margem de segurança (cm)",
    min_value=0.0,
    value=2.0
)

escala_svg = st.slider(
    "Escala do SVG",
    0.1,
    2.0,
    0.35,
    0.05
)

svg_files = st.file_uploader(
    "Upload dos moldes SVG",
    type=["svg"],
    accept_multiple_files=True
)

cores = [
    "#ff69c9",
    "#00c8ff",
    "#00ff99",
    "#ffd700",
    "#9b59b6",
    "#ff5733",
    "#2ecc71",
    "#3498db",
    "#f39c12"
]

ROTACOES = [0, 90, 180]


def extrair_poligonos_svg(svg_path):

    paths, _ = svg2paths(svg_path)

    polygons = []

    for path in paths:

        pontos = []

        for seg in path:

            pontos.append((
                seg.start.real,
                -seg.start.imag
            ))

        if len(pontos) < 3:
            continue

        try:

            poly = Polygon(pontos)

            if poly.area <= 1:
                continue

            if not poly.is_valid:
                poly = poly.buffer(0)

            minx, miny, maxx, maxy = poly.bounds

            poly = translate(
                poly,
                xoff=-minx,
                yoff=-miny
            )

            poly = scale(
                poly,
                xfact=escala_svg,
                yfact=escala_svg,
                origin=(0, 0)
            )

            polygons.append(poly)

        except:
            pass

    return polygons


def colisao(poly, colocadas):

    for p in colocadas:

        if poly.buffer(margem).intersects(
            p["poly"].buffer(margem)
        ):
            return True

    return False


def gerar_pontos(colocadas):

    pontos = [(0, 0)]

    for p in colocadas:

        minx, miny, maxx, maxy = p["poly"].bounds

        pontos.extend([
            (maxx + margem, miny),
            (minx, maxy + margem),
            (maxx + margem, maxy + margem)
        ])

    pontos = sorted(
        pontos,
        key=lambda k: (k[1], k[0])
    )

    return pontos


def nesting(polys):

    colocadas = []
    sobras = []

    for item in polys:

        nome = item["nome"]
        base_poly = item["poly"]

        encaixou = False

        for rot in ROTACOES:

            poly_rot = rotate(
                base_poly,
                rot,
                origin=(0, 0)
            )

            minx, miny, maxx, maxy = poly_rot.bounds

            largura = maxx - minx
            altura = maxy - miny

            pontos = gerar_pontos(colocadas)

            for px, py in pontos:

                movido = translate(
                    poly_rot,
                    xoff=px - minx,
                    yoff=py - miny
                )

                bx1, by1, bx2, by2 = movido.bounds

                if (
                    bx1 < 0 or
                    by1 < 0 or
                    bx2 > largura_tecido or
                    by2 > altura_tecido
                ):
                    continue

                if not colisao(movido, colocadas):

                    colocadas.append({
                        "nome": nome,
                        "poly": movido,
                        "cor": random.choice(cores)
                    })

                    encaixou = True
                    break

            if encaixou:
                break

        if not encaixou:
            sobras.append(nome)

    return colocadas, sobras


if svg_files:

    st.subheader("Preview dos moldes")

    cols = st.columns(4)

    for i, arquivo in enumerate(svg_files):

        with cols[i % 4]:

            st.write(arquivo.name)

            svg_text = arquivo.getvalue().decode()

            st.image(svg_text, use_container_width=True)


if st.button("Gerar Layout Inteligente"):

    if not svg_files:
        st.warning("Envie SVGs")
        st.stop()

    with st.spinner("Calculando encaixe..."):

        polys = []

        for arquivo in svg_files:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".svg"
            ) as tmp:

                tmp.write(arquivo.read())
                caminho = tmp.name

            polygons = extrair_poligonos_svg(caminho)

            for poly in polygons:

                for _ in range(quantidade):

                    polys.append({
                        "nome": arquivo.name.replace(".svg", ""),
                        "poly": poly
                    })

        polys = sorted(
            polys,
            key=lambda p: p["poly"].area,
            reverse=True
        )

        colocadas, sobras = nesting(polys)

        fig, ax = plt.subplots(figsize=(16, 9))

        fig.patch.set_facecolor("#111111")
        ax.set_facecolor("#111111")

        tecido = patches.Rectangle(
            (0, 0),
            largura_tecido,
            altura_tecido,
            fill=False,
            edgecolor="white",
            linewidth=2
        )

        ax.add_patch(tecido)

        for item in colocadas:

            poly = item["poly"]

            coords = np.array(poly.exterior.coords)

            patch = patches.Polygon(
                coords,
                closed=True,
                facecolor=item["cor"],
                edgecolor="white",
                linewidth=1.2,
                alpha=0.85
            )

            ax.add_patch(patch)

            centro = poly.centroid

            ax.text(
                centro.x,
                centro.y,
                item["nome"],
                ha="center",
                va="center",
                fontsize=7,
                color="white"
            )

        ax.set_xlim(0, largura_tecido)
        ax.set_ylim(0, altura_tecido)
        ax.set_aspect("equal")

        st.pyplot(fig)

        area_usada = sum([
            p["poly"].area
            for p in colocadas
        ])

        area_total = largura_tecido * altura_tecido

        desperdicio = area_total - area_usada

        aproveitamento = (
            area_usada / area_total
        ) * 100

        st.subheader("Resultado")

        c1, c2 = st.columns(2)

        with c1:

            st.write(f"Peças colocadas: {len(colocadas)}")
            st.write(f"Área usada: {area_usada:.2f}")
            st.write(f"Desperdício: {desperdicio:.2f}")
            st.write(f"Aproveitamento: {aproveitamento:.2f}%")

        with c2:

            contador = Counter()

            for p in colocadas:
                contador[p["nome"]] += 1

            st.write("Repetições")

            for nome, qtd in contador.items():
                st.write(f"{nome}: {qtd}x")

            st.write("Peças não colocadas")

            if len(sobras) == 0:
                st.write("Nenhuma")
            else:
                for s in sobras:
                    st.write(s)