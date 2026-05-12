import streamlit as st
from collections import Counter

def mostrar_resultados(
    dados,
    colocadas,
    sobras
):

    st.subheader("Resultado")

    c1, c2 = st.columns(2)

    with c1:

        st.write(
            f"Área usada: {dados['area_usada']:.2f}"
        )

        st.write(
            f"Desperdício: {dados['desperdicio']:.2f}"
        )

        st.write(
            f"Aproveitamento: {dados['aproveitamento']:.2f}%"
        )

    with c2:

        contador = Counter()

        for p in colocadas:
            contador[p["nome"]] += 1

        st.write("Repetições")

        for nome, qtd in contador.items():
            st.write(f"{nome}: {qtd}x")

        st.write("Sobras")

        if len(sobras) == 0:
            st.write("Nenhuma")

        else:

            for s in sobras:
                st.write(s)