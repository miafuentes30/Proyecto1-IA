import streamlit as st
from modulos.config import cargar_configuracion
from modulos.procesamiento import generar_resumen
from modulos.vista import mostrar_resultados, generar_nube_palabras
import time

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
                raw_result = agent.invoke({"input": tema})
                
                # Verificamos si `raw_result` es una lista de Document o algo similar
                if isinstance(raw_result, list) and all(hasattr(d, "page_content") for d in raw_result):
                    respuesta = []
                    for doc in raw_result:
                        respuesta.append({
                            "title": doc.metadata.get("title", "Sin título"),
                            "url": doc.metadata.get("source", "#"),
                            "content": doc.page_content
                        })
                elif isinstance(raw_result, dict) and "output" in raw_result:
                    # Si es un dict con "output" (puede que la IA devuelva un texto "encapsulado")
                    respuesta = [{
                        "title": "Respuesta",
                        "url": "#",
                        "content": raw_result["output"]
                    }]
                else:
                    # Cualquier otro caso: asumimos un string suelto
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

        # Mostrar los resultados
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
