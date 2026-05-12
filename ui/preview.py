import streamlit as st

def mostrar_preview(svg_files):

    st.subheader("Preview dos moldes")

    cols = st.columns(4)

    for i, arquivo in enumerate(svg_files):

        with cols[i % 4]:

            st.write(arquivo.name)

            svg_text = arquivo.getvalue().decode()

            st.image(
                svg_text,
                use_container_width=True
            )