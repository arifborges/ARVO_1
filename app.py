import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

st.set_page_config(page_title="ARVO 3.0", layout="wide")

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

st.title("ARVO 3.0 - Corte Inteligente")

largura_tecido = st.number_input("Largura do tecido", min_value=60, value=120)
altura_tecido = st.number_input("Altura do tecido", min_value=60, value=90)

modelo = st.selectbox(
    "Modelo",
    ["Camiseta M", "Camiseta G", "Calça", "Saia"]
)

quantidade = st.number_input("Quantidade", min_value=1, value=2)

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

def tentar_layout(pecas, largura, altura):

    espacos = [(0, 0, largura, altura)]
    colocadas = []
    area = 0
    nao_colocadas = []

    for peca in pecas:

        nome, w0, h0 = peca
        encaixou = False

        for i in range(len(espacos)):

            ex, ey, ew, eh = espacos[i]

            opcoes = [(w0, h0), (h0, w0)]

            for w, h in opcoes:

                if w <= ew and h <= eh:

                    colocadas.append((nome, ex, ey, w, h))
                    area += w * h

                    del espacos[i]

                    direita = (ex + w, ey, ew - w, h)
                    cima = (ex, ey + h, ew, eh - h)

                    if direita[2] > 3 and direita[3] > 3:
                        espacos.append(direita)

                    if cima[2] > 3 and cima[3] > 3:
                        espacos.append(cima)

                    espacos = sorted(
                        espacos,
                        key=lambda x: x[2] * x[3],
                        reverse=True
                    )

                    encaixou = True
                    break

            if encaixou:
                break

        if not encaixou:
            nao_colocadas.append(nome)

    return colocadas, area, nao_colocadas, espacos

if st.button("Gerar Melhor Layout"):

    pecas = []

    for _ in range(quantidade):
        pecas.extend(gerar_pecas(modelo))

    melhor = None
    melhor_area = 0

    for _ in range(30):

        random.shuffle(pecas)

        teste = sorted(
            pecas,
            key=lambda x: x[1] * x[2],
            reverse=random.choice([True, False])
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
    ax.set_facecolor("#111111")

    tecido = patches.Rectangle(
        (0,0),
        largura_tecido,
        altura_tecido,
        fill=False,
        edgecolor="white",
        linewidth=2
    )

    ax.add_patch(tecido)

    cores = [
        "#ff69c9","#00c8ff","#00ff99",
        "#ffd700","#9b59b6","#ff5733",
        "#2ecc71","#3498db","#f39c12"
    ]

    for i, item in enumerate(colocadas):

        nome, x, y, w, h = item
        cor = cores[i % len(cores)]

        if nome in ["Frente", "Costas"]:
            pontos = [
                (x+2, y),
                (x+w-2, y),
                (x+w, y+h),
                (x, y+h)
            ]
            bloco = patches.Polygon(
                pontos,
                closed=True,
                facecolor=cor,
                edgecolor="white",
                alpha=0.8
            )

        elif nome == "Manga":
            pontos = [
                (x+2, y),
                (x+w-2, y),
                (x+w, y+h),
                (x, y+h)
            ]
            bloco = patches.Polygon(
                pontos,
                closed=True,
                facecolor=cor,
                edgecolor="white",
                alpha=0.8
            )

        else:
            bloco = patches.Rectangle(
                (x,y),
                w,
                h,
                facecolor=cor,
                edgecolor="white",
                alpha=0.8
            )

        ax.add_patch(bloco)

        ax.text(
            x + w/2,
            y + h/2,
            nome,
            ha="center",
            va="center",
            fontsize=8,
            color="white"
        )

    for sobra in espacos:

        sx, sy, sw, sh = sobra

        bloco = patches.Rectangle(
            (sx, sy),
            sw,
            sh,
            fill=False,
            linestyle="dashed",
            edgecolor="#666666"
        )

        ax.add_patch(bloco)

    ax.set_xlim(0, largura_tecido)
    ax.set_ylim(0, altura_tecido)
    ax.set_aspect("equal")

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