import streamlit as st

def carregar_css():

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
    }
    </style>
    """, unsafe_allow_html=True)