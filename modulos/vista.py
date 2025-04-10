import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re
import numpy as np

def mostrar_resultados(resultados, config=None):
    if not resultados:
        st.warning("No se encontraron resultados.")
        return
    
    for i, resultado in enumerate(resultados):
        # Verificar si el resultado es un string
        if isinstance(resultado, str):
            st.markdown(f"<div class='result-card'>", unsafe_allow_html=True)
            st.markdown("### Respuesta del Sistema")
            st.markdown(resultado)
            st.markdown("</div>", unsafe_allow_html=True)
            continue
        
        # Para resultados estructurados
        try:
            # Extraer título y URL si están disponibles
            titulo = resultado.get('title', f"Resultado #{i+1}")
            url = resultado.get('url', '#')
            contenido = resultado.get('content', 'No hay contenido disponible.')
            
            # Mostrar cada resultado en una tarjeta
            st.markdown(f"<div class='result-card'>", unsafe_allow_html=True)
            
            # Título con enlace
            st.markdown(f"### [{titulo}]({url})")
            
            # Contenido truncado
            contenido_truncado = contenido[:500] + "..." if len(contenido) > 500 else contenido
            st.code(contenido_truncado, language="")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error al mostrar resultado {i+1}")

def generar_nube_palabras(resultados):
    # Extraer texto de los resultados
    texto_completo = ""
    
    for resultado in resultados:
        if isinstance(resultado, str):
            texto_completo += resultado + " "
        else:
            if 'content' in resultado:
                texto_completo += resultado['content'] + " "
            if 'title' in resultado:
                texto_completo += resultado['title'] + " "

    texto_completo = texto_completo.lower()
    texto_completo = re.sub(r'[^\w\s]', '', texto_completo)
    
    # Stopwords en español e inglés
    stopwords = set(STOPWORDS)
    custom_stopwords = {'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 
                       'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 
                       'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'ha', 'sí', 'esta', 
                       'the', 'and', 'of', 'to', 'in', 'is', 'it', 'that', 'for', 'with'}
    stopwords.update(custom_stopwords)
    
    # Crear WordCloud
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
    
    # Crear figura para visualizar
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_facecolor('black')
    fig.tight_layout(pad=0)
    fig.patch.set_facecolor('black')
    
    return fig