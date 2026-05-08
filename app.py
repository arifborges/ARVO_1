# ARVO 4.0

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from svgpathtools import svg2paths
from shapely.geometry import Polygon
from shapely import affinity
import numpy as np
import random

st.set_page_config(page_title="ARVO 4.0", layout="wide")

st.markdown("""
<style>
.stApp{background:#000;color:white;}
h1,h2,h3,p,label{color:white!important;}
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
}
</style>
""", unsafe_allow_html=True)

st.title("ARVO 4.0 - Corte Inteligente com SVG")

largura_tecido = st.number_input("Largura do tecido", min_value=60, value=140)
altura_tecido = st.number_input("Altura do tecido", min_value=60, value=100)

modelo = st.selectbox(
    "Modelo Base",
    ["Camiseta M", "Camiseta G", "Calça", "Saia"]
)

quantidade = st.number_input("Quantidade", min_value=1, value=2)

svg_file = st.file_uploader("Importar molde SVG", type=["svg"])

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

def gerar_pecas(nome):

    if nome == "Camiseta M":
        return [
            ("Frente", 28, 38),
            ("Costas", 28, 38),
            ("Manga", 18, 22),
            ("Manga", 18, 22),
            ("Gola", 14, 6)
        ]

    if nome == "Camiseta G":
        return [
            ("Frente", 32, 42),
            ("Costas", 32, 42),
            ("Manga", 22, 24),
            ("Manga", 22, 24),
            ("Gola", 16, 7)
        ]

    if nome == "Calça":
        return [
            ("Perna", 24, 50),
            ("Perna", 24, 50),
            ("Bolso", 14, 14),
            ("Bolso", 14, 14),
            ("Cós", 38, 10)
        ]

    if nome == "Saia":
        return [
            ("Frente", 32, 40),
            ("Costas", 32, 40),
            ("Cintura", 30, 8)
        ]

def criar_poligono(nome, x, y, w, h):

    if nome in ["Frente", "Costas"]:
        pontos = [
            (x+2, y),
            (x+w-2, y),
            (x+w, y+h),
            (x, y+h)
        ]

    elif nome == "Manga":
        pontos = [
            (x+3, y),
            (x+w-3, y),
            (x+w, y+h),
            (x, y+h)
        ]

    else:
        pontos = [
            (x, y),
            (x+w, y),
            (x+w, y+h),
            (x, y+h)
        ]

    return Polygon(pontos)

def tentar_layout(pecas, largura, altura):

    espacos = [(0,0,largura,altura)]
    colocadas = []
    area = 0
    sobras = []

    for peca in pecas:

        nome, w0, h0 = peca
        encaixou = False

        for i in range(len(espacos)):

            ex, ey, ew, eh = espacos[i]

            for w, h in [(w0,h0),(h0,w0)]:

                if w <= ew and h <= eh:

                    colocadas.append((nome, ex, ey, w, h))
                    area += w*h

                    del espacos[i]

                    direita = (ex+w, ey, ew-w, h)
                    cima = (ex, ey+h, ew, eh-h)

                    if direita[2] > 4 and direita[3] > 4:
                        espacos.append(direita)

                    if cima[2] > 4 and cima[3] > 4:
                        espacos.append(cima)

                    espacos = sorted(
                        espacos,
                        key=lambda x: x[2]*x[3],
                        reverse=True
                    )

                    encaixou = True
                    break

            if encaixou:
                break

        if not encaixou:
            sobras.append(nome)

    return colocadas, area, sobras, espacos

def desenhar_svg(ax, svg_path, offset_x, offset_y, escala=1):

    paths, attributes = svg2paths(svg_path)

    for path in paths:

        pontos = []

        for segment in path:
            pontos.append((
                segment.start.real * escala + offset_x,
                -segment.start.imag * escala + offset_y
            ))

        if len(pontos) > 2:
            patch = patches.Polygon(
                pontos,
                closed=True,
                fill=False,
                edgecolor="#00ffff",
                linewidth=1.5
            )

            ax.add_patch(patch)

if st.button("Gerar Melhor Layout"):

    pecas = []

    for _ in range(quantidade):
        pecas.extend(gerar_pecas(modelo))

    melhor = None
    melhor_area = 0

    for _ in range(40):

        random.shuffle(pecas)

        teste = sorted(
            pecas,
            key=lambda x: x[1]*x[2],
            reverse=random.choice([True,False])
        )

        resultado = tentar_layout(
            teste,
            largura_tecido,
            altura_tecido
        )

        if resultado[1] > melhor_area:
            melhor = resultado
            melhor_area = resultado[1]

    colocadas, area_usada, sobras, espacos = melhor

    fig, ax = plt.subplots(figsize=(14,8))

    tecido = patches.Rectangle(
        (0,0),
        largura_tecido,
        altura_tecido,
        fill=False,
        edgecolor="white",
        linewidth=2
    )

    ax.add_patch(tecido)

    for i, item in enumerate(colocadas):

        nome, x, y, w, h = item
        cor = cores[i % len(cores)]

        poly = criar_poligono(nome, x, y, w, h)

        coords = np.array(poly.exterior.coords)

        patch = patches.Polygon(
            coords,
            closed=True,
            facecolor=cor,
            edgecolor="white",
            alpha=0.8
        )

        ax.add_patch(patch)

        ax.text(
            x+w/2,
            y+h/2,
            nome,
            ha="center",
            va="center",
            fontsize=8,
            color="white"
        )

    for sobra in espacos:

        sx, sy, sw, sh = sobra

        bloco = patches.Rectangle(
            (sx,sy),
            sw,
            sh,
            fill=False,
            linestyle="dashed",
            edgecolor="#555555"
        )

        ax.add_patch(bloco)

    if svg_file:

        with open("molde_temp.svg", "wb") as f:
            f.write(svg_file.read())

        desenhar_svg(ax, "molde_temp.svg", 5, altura_tecido-5, 0.2)

    ax.set_xlim(0, largura_tecido)
    ax.set_ylim(0, altura_tecido)
    ax.set_aspect("equal")
    ax.set_facecolor("#111111")

    st.pyplot(fig)

    area_total = largura_tecido * altura_tecido
    desperdicio = area_total - area_usada
    aproveitamento = (area_usada / area_total) * 100

    st.subheader("Resultado")

    c1, c2 = st.columns(2)

    with c1:
        st.write(f"Peças colocadas: {len(colocadas)}")
        st.write(f"Área usada: {area_usada}")
        st.write(f"Desperdício: {desperdicio}")
        st.write(f"Aproveitamento: {aproveitamento:.2f}%")

    with c2:
        st.write("Peças não colocadas:")

        if len(sobras) == 0:
            st.write("Nenhuma")
        else:
            for s in sobras:
                st.write(s)