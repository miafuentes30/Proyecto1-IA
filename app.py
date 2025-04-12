import json
import streamlit as st
from modulos.config import cargar_configuracion
from modulos.procesamiento import generar_resumen
from modulos.vista import mostrar_resultados, generar_nube_palabras
import time

import re

# Limpia etiquetas Markdown como ```json ... ```
def limpiar_bloque_json(texto):
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", texto.strip(), flags=re.IGNORECASE)

# Configuración de la página
st.set_page_config(
    page_title="CyberResearch Assistant",
    layout="wide"
)

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Archivo de estilo '{file_name}' no encontrado.")

local_css("style.css")

# Fondo personalizado
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
    # Cargar configuración y construir el agente ReAct
    config = cargar_configuracion()
    # Parámetros adicionales de configuración
    config["max_results"] = 5
    config["depth"] = "moderate"
    config["include_images"] = True
    config["processing_speed"] = 5

    st.markdown('<h1 class="title-effect">🖥️ CyberResearch Assistant 🖥️</h1>', unsafe_allow_html=True)
    st.markdown('<div class="highlight-text">Sistema de investigación automatizado con IA - Mia Fuentes & June Herrera</div>', unsafe_allow_html=True)
    
    # Agregar label no vacío en el text_input
    tema = st.text_input("Tema:", placeholder="Ingrese el tema que desea investigar...")
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        buscar = st.button("EJECUTAR", use_container_width=True)

    if buscar and tema:
        st.session_state["start_time"] = time.time()
        with st.spinner("Buscando información en la web…"):
            try:
                agent = config["langchain_agent"]
                input_usuario = f"""
                Quiero que actúes como un investigador experto. Usa herramientas externas disponibles para buscar y analizar información actualizada.

                Tema: "{tema}"

                Devuelve los resultados en el siguiente formato JSON (mínimo 5 entradas):
                [
                    {{
                        "title": "Título del artículo",
                        "url": "https://...",
                        "content": "Contenido en español, al menos 4 párrafos con información detallada"
                    }},
                    ...
                ]
                """
                raw_result = agent.invoke({"input": input_usuario})
                print(raw_result) 
                
                # Intentamos parsear directamente el JSON que devuelve la clave "output" (o raw_result si ya es string)
                try:
                    if isinstance(raw_result, dict) and "output" in raw_result:
                        respuesta = json.loads(limpiar_bloque_json(raw_result["output"]))
                    else:
                        respuesta = json.loads(raw_result)
                    
                    # Validamos que la respuesta sea una lista de diccionarios
                    if not isinstance(respuesta, list):
                        raise ValueError("La respuesta JSON no es una lista")
                
                except Exception as e:
                    st.warning(f"No se pudo parsear el resultado JSON. Se muestra la respuesta en bruto. Error: {e}")
                    respuesta = [{
                        "title": "Respuesta",
                        "url": "#",
                        "content": str(raw_result)
                    }]
                    
            except Exception as e:
                st.error(f"Ocurrió un error al ejecutar el agente: {e}")
                return

        if not respuesta:
            st.warning("No se encontraron resultados para ese tema.")
            return

        # Mostrar los resultados (aquí asegúrate de que la función mostrar_resultados espere el formato adecuado)
        st.subheader("Resultados encontrados")
        mostrar_resultados(respuesta)

        with st.spinner("Generando resumen…"):
            resumen = generar_resumen(respuesta, config=config)
        st.subheader("Resumen automático")
        st.markdown(resumen)

        with st.spinner("Generando nube de palabras…"):
            wordcloud = generar_nube_palabras([respuesta])
        st.subheader("Nube de palabras")
        st.pyplot(wordcloud)

        tiempo_total = round(time.time() - st.session_state["start_time"], 2)
        st.markdown(f"*Búsqueda completada en {tiempo_total} segundos.*")

if __name__ == "__main__":
    main()
