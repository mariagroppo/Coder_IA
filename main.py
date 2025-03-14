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
        response = requests.get(url, timeout=10)  # Agrega un tiempo de espera
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

# Interfaz de Streamlit (mejorada)
st.title("Resumidor de Noticias con Gemini")

url = st.text_input("Ingresa la URL de la noticia:")

# Selección del modelo
modelo_seleccionado = st.selectbox("Selecciona el modelo Gemini:", ['gemini-2.0-flash', 'gemini-2.0-pro'])

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