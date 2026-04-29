import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

st.set_page_config(page_title="ARVO", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: white;
}

h1,h2,h3,p,label {
    color: white !important;
}

div[data-baseweb="input"] > div {
    background-color: #1a1a1a;
    border: 1px solid #ff69c9;
    border-radius: 10px;
}

.stButton>button {
    background: linear-gradient(135deg,#ff69c9,#1a1a1a);
    color: white;
    border-radius: 12px;
    border: 1px solid #ff69c9;
    padding: 12px 25px;
    font-size: 18px;
}

.stButton>button:hover {
    border: 1px solid white;
}
</style>
""", unsafe_allow_html=True)

st.title("ARVO - Otimização de Corte Têxtil")

largura_tecido = st.number_input("Largura do tecido", min_value=1, value=100)
altura_tecido = st.number_input("Altura do tecido", min_value=1, value=80)

st.subheader("Adicionar moldes")

qtd = st.number_input("Quantidade de moldes", min_value=1, value=3)

moldes = []

for i in range(qtd):
    col1, col2 = st.columns(2)

    with col1:
        w = st.number_input(
            f"Largura molde {i+1}",
            min_value=1,
            value=20,
            key=f"w{i}"
        )

    with col2:
        h = st.number_input(
            f"Altura molde {i+1}",
            min_value=1,
            value=10,
            key=f"h{i}"
        )

    moldes.append((w, h))

if st.button("Gerar Layout"):

    moldes.sort(key=lambda x: x[0] * x[1], reverse=True)

    fig, ax = plt.subplots(figsize=(10, 7))

    tecido = patches.Rectangle(
        (0, 0),
        largura_tecido,
        altura_tecido,
        fill=False,
        linewidth=2,
        edgecolor="white"
    )

    ax.add_patch(tecido)

    x = 0
    y = 0
    linha_altura = 0
    area_usada = 0
    colocados = 0
    sobras = []

    cores = [
        "#ff69c9", "#00ffff", "#00ff99",
        "#ffd700", "#ff5733", "#9b59b6",
        "#3498db", "#2ecc71", "#f39c12"
    ]

    for i, molde in enumerate(moldes):
        w, h = molde
        rotacionado = False

        if x + w > largura_tecido and x + h <= largura_tecido:
            w, h = h, w
            rotacionado = True

        if x + w > largura_tecido:
            x = 0
            y += linha_altura
            linha_altura = 0

            if x + w > largura_tecido and x + h <= largura_tecido:
                w, h = h, w
                rotacionado = True

        if y + h <= altura_tecido:

            cor = cores[i % len(cores)]

            bloco = patches.Rectangle(
                (x, y),
                w,
                h,
                facecolor=cor,
                alpha=0.75,
                edgecolor="white"
            )

            ax.add_patch(bloco)

            texto = f"{w}x{h}"
            if rotacionado:
                texto += " ↻"

            ax.text(
                x + w / 2,
                y + h / 2,
                texto,
                ha="center",
                va="center",
                fontsize=8,
                color="white"
            )

            x += w
            linha_altura = max(linha_altura, h)

            area_usada += w * h
            colocados += 1

        else:
            sobras.append((w, h))

    ax.set_xlim(0, largura_tecido)
    ax.set_ylim(0, altura_tecido)
    ax.set_aspect("equal")
    ax.set_facecolor("#111111")

    st.pyplot(fig)

    area_total = largura_tecido * altura_tecido
    desperdicio = area_total - area_usada
    aproveitamento = (area_usada / area_total) * 100

    st.subheader("Resultado")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Moldes colocados: {colocados}")
        st.write(f"Área usada: {area_usada}")
        st.write(f"Desperdício: {desperdicio}")
        st.write(f"Aproveitamento: {aproveitamento:.2f}%")

    with col2:
        st.write(f"Moldes não colocados: {len(sobras)}")

        if len(sobras) > 0:
            for item in sobras:
                st.write(f"{item[0]} x {item[1]}")