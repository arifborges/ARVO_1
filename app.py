import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="ARVO 2.0", layout="wide")

st.markdown("""
<style>
.stApp {background-color:#000000;color:white;}
h1,h2,h3,p,label {color:white !important;}
div[data-baseweb="input"] > div {
    background:#1a1a1a;
    border:1px solid #ff69c9;
    border-radius:10px;
}
.stButton>button{
    background:linear-gradient(135deg,#ff69c9,#1a1a1a);
    color:white;
    border-radius:12px;
    border:1px solid #ff69c9;
    padding:12px 24px;
}
</style>
""", unsafe_allow_html=True)

st.title("ARVO 2.0 - Moldes Inteligentes")

largura_tecido = st.number_input("Largura do tecido", min_value=50, value=120)
altura_tecido = st.number_input("Altura do tecido", min_value=50, value=90)

tipo = st.selectbox(
    "Tipo de roupa",
    ["Camiseta", "Calça", "Saia"]
)

quantidade = st.number_input("Quantidade", min_value=1, value=2)

def gerar_pecas(tipo):

    if tipo == "Camiseta":
        return [
            ("Frente", 26, 35),
            ("Costas", 26, 35),
            ("Manga", 18, 15),
            ("Manga", 18, 15),
            ("Gola", 12, 6)
        ]

    if tipo == "Calça":
        return [
            ("Perna", 20, 45),
            ("Perna", 20, 45),
            ("Bolso", 12, 12),
            ("Bolso", 12, 12),
            ("Cós", 35, 8)
        ]

    if tipo == "Saia":
        return [
            ("Frente", 30, 35),
            ("Costas", 30, 35),
            ("Cintura", 28, 8)
        ]

if st.button("Gerar Layout"):

    moldes = []

    for _ in range(quantidade):
        moldes.extend(gerar_pecas(tipo))

    moldes.sort(key=lambda x: x[1] * x[2], reverse=True)

    fig, ax = plt.subplots(figsize=(12,8))

    tecido = patches.Rectangle(
        (0,0),
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
        "#ff69c9","#00ffff","#00ff99",
        "#ffd700","#9b59b6","#3498db",
        "#e74c3c","#2ecc71","#f39c12"
    ]

    for i, molde in enumerate(moldes):

        nome = molde[0]
        w = molde[1]
        h = molde[2]

        rotacionado = False

        if x + w > largura_tecido and x + h <= largura_tecido:
            w, h = h, w
            rotacionado = True

        if x + w > largura_tecido:
            x = 0
            y += linha_altura
            linha_altura = 0

        if y + h <= altura_tecido:

            cor = cores[i % len(cores)]

            if nome in ["Frente", "Costas"]:
                pontos = [
                    (x, y),
                    (x + w, y),
                    (x + w - 3, y + h),
                    (x + 3, y + h)
                ]

                bloco = patches.Polygon(
                    pontos,
                    closed=True,
                    facecolor=cor,
                    edgecolor="white",
                    alpha=0.75
                )

            elif nome == "Manga":
                pontos = [
                    (x, y),
                    (x + w, y),
                    (x + w - 4, y + h),
                    (x + 4, y + h)
                ]

                bloco = patches.Polygon(
                    pontos,
                    closed=True,
                    facecolor=cor,
                    edgecolor="white",
                    alpha=0.75
                )

            else:
                bloco = patches.Rectangle(
                    (x,y),
                    w,
                    h,
                    facecolor=cor,
                    edgecolor="white",
                    alpha=0.75
                )

            ax.add_patch(bloco)

            texto = nome
            if rotacionado:
                texto += " ↻"

            ax.text(
                x + w/2,
                y + h/2,
                texto,
                ha="center",
                va="center",
                fontsize=7,
                color="white"
            )

            x += w
            linha_altura = max(linha_altura, h)

            area_usada += w * h
            colocados += 1

        else:
            sobras.append(nome)

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
        st.write(f"Peças colocadas: {colocados}")
        st.write(f"Área usada: {area_usada}")
        st.write(f"Desperdício: {desperdicio}")
        st.write(f"Aproveitamento: {aproveitamento:.2f}%")

    with col2:
        st.write(f"Peças não colocadas: {len(sobras)}")

        for item in sobras:
            st.write(item)