import streamlit as st
from modulos.procesamiento import generar_resumen
from modulos.vista import mostrar_resultados, generar_nube_palabras
from modulos.config import cargar_configuracion
import time

# Configuración de la página
st.set_page_config(
    page_title="CyberResearch Assistant",
    layout="wide"
)

# CSS 
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

local_css("style.css")

# Fondo 
st.markdown("""
<style>
    .reportview-container {
        background-color: #0a0a0a;
        background-image: 
            radial-gradient(rgba(0, 255, 0, 0.1) 1px, transparent 1px),
            radial-gradient(rgba(0, 255, 0, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        background-position: 0 0, 25px 25px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Cargar configuración
    config["max_results"] = 5
    config["depth"] = "moderate"
    config["include_images"] = True
    config["processing_speed"] = 5

    # Encabezado centrado
    st.markdown('<h1 class="title-effect">🖥️ CyberResearch Assistant 🖥️</h1>', unsafe_allow_html=True)
    st.markdown('<div class="highlight-text">Sistema de investigación automatizado con IA - Mia Fuentes & June Herrera</div>', unsafe_allow_html=True)

    tema = st.text_input("", placeholder="Ingrese el tema que desea investigar...")

    # Espaciado 
    st.markdown("<br>", unsafe_allow_html=True)

    # Botón ejecutar 
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        buscar = st.button("EJECUTAR", use_container_width=True)


    st.markdown('</div>', unsafe_allow_html=True)

    # Lógica de búsqueda
# JUNE ACA PONES LO TUYO :3

if __name__ == "__main__":
    main()
