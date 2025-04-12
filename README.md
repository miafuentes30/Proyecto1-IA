# Proyecto-1---IA

# INSTRUCCIONES PARA LA EJECUCIÓN

Pasos para configurar el entorno

    1. Clonar el repositorio: 
    git clone https://github.com/miafuentes30/Proyecto1-IA.git

    2. Crear un entorno virtual:
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

    3. Instalar dependencias:
    pip install -r requirements.txt
    pip install matplotlib wordcloud langchain openai python-dotenv requests streamlit tavily-python

    4. Para ejecutar el programa:
    streamlit run app.py


# DESCRIPCIÓN DE MÓDULOS

1. app.py:

Este es el módulo principal que contiene la interfaz de usuario con Streamlit, cual maneja la configuración de la página, entrada del usuario, coordinación de los otros módulos y visualización de resultados.

2. config.py:

Este se encarga de cargar variables de entorno, configurar el agente LangChain, inicializar las herramientas de búsqueda y establecer parámetros del modelo LLM.

3. procesamiento.py:

Contiene funciones para generar resúmenes del contenido usando OpenAI y procesar la respuesta del modelo de lenguaje

4. vista.py:

Este es el módulo de visualización que funciona para mostrar resultados en formato de tarjetas, generar nubes de palabras, aplicar estilos CSS personalizados.

5. style.css:

Archivo de estilos que define el tema oscuro, las animaciones y transiciones, y el diseño responsive.


# REFLEXIÓN


La inteligencia artificial ha cambiado la forma de pensar de las personas, ofreciendo todo tipo de información a la mano y herramientas para facilitar las tareas que antes requerían horas de investigación. Actualmene, la IA puede facilitar la recopilación de datos, generar resumenes bien redactados e identificar patrones a través de visualizaciones como nubes de palabras. Así como la IA tiene sus aspectos positivos, también tiene aspectos negativos como es la dependencia excesiva del mismo, ya que hay que tomar en cuenta que pueden propagar información errónea si no se validan sus fuentes o si los algoritmos están sesgados, por otra parte, algunos modelos de lenguaje como GPT-4 unicamente concluyen sin saber de donde recabaron esta información. Además, la IA no tiene el juicio  humano y eso puede llevar a priorizar fuentes populares sobre fuentes confiables o malinterpretar contextos culturales y lingüísticos.

También hay que tomar en cuenta el tema del reemplazo de habilidades humanas; la IA puede acelerar procesos y podría reducir el pensamiento crítico y capacidad de análisis en las personas. Consideramos que el equilibrio ideal sería usar las IAs como asistentes, manteniendo siempre una supervisión humana que cuestione, refine y complemente los resultados generados automáticamente por la misma.