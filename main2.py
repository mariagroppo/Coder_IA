import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Cargar la clave API desde el archivo .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configurar la clave API de Gemini
genai.configure(api_key=api_key)

# Función para extraer el texto de una URL (mejorada)
def extraer_texto_de_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        texto = ' '.join([p.text for p in soup.find_all('p')])
        return texto
    except requests.exceptions.RequestException as e:
        return f"Error al acceder a la URL: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

# Función para resumir el texto utilizando Gemini (configurable)
def resumir_texto(texto, modelo='gemini-2.0-flash'):
    model = genai.GenerativeModel(modelo)
    try:
        response = model.generate_content(f"Resumir el siguiente texto: {texto}")
        return response.text
    except Exception as e:
        return f"Error al resumir el texto: {e}"

# Configuración de la página
st.set_page_config(page_title="Resumidor de Noticias con Gemini", layout="wide")

# Paleta de colores
primary_color = "#4CAF50"
secondary_color = "#2196F3"
background_color = "#F5F5F5"

# Header
st.markdown(
    f"""
    <div style="background-color:{primary_color};padding:20px;border-radius:10px;">
        <h1 style="color:white;text-align:center;">Resumidor de Noticias con Gemini</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Descripción y "Cómo funciona"
st.markdown(
    f"""
    <div style="background-color:{background_color};padding:20px;border-radius:10px;margin-top:20px;">
        <h2>Descripción</h2>
        <p>Esta aplicación utiliza el modelo Gemini de Google para resumir noticias a partir de URLs.</p>
        <h2>Cómo funciona</h2>
        <p>1. Ingresa la URL de la noticia en el campo de texto.</p>
        <p>2. Selecciona el modelo Gemini que deseas utilizar.</p>
        <p>3. Haz clic en el botón "Resumir".</p>
        <p>4. La aplicación extraerá el texto de la noticia y generará un resumen utilizando el modelo Gemini seleccionado.</p>
        <p>5. El resumen se mostrará en la página.</p>
        <p>Puedes desplegar esta app desde <a href="https://streamlit.io">Streamlit Community Cloud</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Interfaz de Streamlit
st.markdown(
    f"""
    <div style="background-color:white;padding:20px;border-radius:10px;margin-top:20px;">
        <h2>Resumir Noticia</h2>
        <p>Ingresa la URL de la noticia:</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Campo de texto para la URL
url = st.text_input("", key="url")

# Selección del modelo
modelo_seleccionado = st.selectbox("Selecciona el modelo Gemini:", ['gemini-2.0-flash', 'gemini-2.0-pro'])

# Botón "Resumir"
if st.button("Resumir"):
    if url:
        with st.spinner("Extrayendo y resumiendo la noticia..."):
            texto_noticia = extraer_texto_de_url(url)
            if "Error" not in texto_noticia:
                resumen = resumir_texto(texto_noticia, modelo_seleccionado)
                st.subheader("Resumen:")
                st.write(resumen)
            else:
                st.error(texto_noticia)
    else:
        st.warning("Por favor, ingresa una URL.")

# Footer
st.markdown(
    f"""
    <div style="background-color:{primary_color};padding:10px;border-radius:10px;margin-top:20px;">
        <p style="color:white;text-align:center;">Desarrollado con Streamlit y Gemini</p>
    </div>
    """,
    unsafe_allow_html=True,
)