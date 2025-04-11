import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re
import numpy as np

def mostrar_resultados(resultados, config=None):
    if not resultados:
        st.warning("No se encontraron resultados.")
        return

    # CSS para estilizar las tarjetas de resultados
    css = """
    <style>
    .result-card {
        background-color: #f2f2f2;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 8px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .result-card h3 {
        margin: 0 0 10px 0;
    }
    .result-card p {
        margin: 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    for i, resultado in enumerate(resultados, start=1):
        if not isinstance(resultado, dict):
            st.error(f"El resultado {i} no tiene el formato esperado.")
            continue

        try:
            titulo = resultado.get('title', f"Resultado {i}")
            url = resultado.get('url', '#')
            contenido = resultado.get('content', 'No hay contenido disponible.')

            st.markdown(f"### <a href='{url}' target='_blank'>{titulo}</a>", unsafe_allow_html=True)
            st.markdown(f"<p>{contenido}</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al mostrar resultado {i}: {e}")




def generar_nube_palabras(resultados):
    texto_completo = ""

    # Asegurarse de que estamos trabajando con una lista plana de resultados
    for resultado in resultados:
        if isinstance(resultado, dict):
            texto_completo += resultado.get('content', '') + " "
            texto_completo += resultado.get('title', '') + " "
        elif isinstance(resultado, str):
            texto_completo += resultado + " "
        elif isinstance(resultado, list):
            # Si es una lista anidada, procesar cada subelemento
            for sub in resultado:
                if isinstance(sub, dict):
                    texto_completo += sub.get('content', '') + " "
                    texto_completo += sub.get('title', '') + " "
                elif isinstance(sub, str):
                    texto_completo += sub + " "

    # Normalizar texto
    texto_completo = texto_completo.lower()
    texto_completo = re.sub(r'[^\w\s]', '', texto_completo)

    # Definir stopwords personalizadas
    stopwords = set(STOPWORDS)
    stopwords.update({
        'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las',
        'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como',
        'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'ha', 'sí', 'esta',
        'the', 'and', 'of', 'to', 'in', 'is', 'it', 'that', 'for', 'with'
    })

    # Generar la WordCloud
    wc = WordCloud(
        width=800,
        height=800,
        background_color='black',
        colormap='Greens',
        stopwords=stopwords,
        max_font_size=100,
        min_font_size=10,
        contour_width=1,
        contour_color='#0f0'
    ).generate(texto_completo)

    # Visualización
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_facecolor('black')
    fig.tight_layout(pad=0)
    fig.patch.set_facecolor('black')

    return fig
