import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

def cargar_configuracion():
    """Carga las variables de entorno y configura los componentes principales"""
    load_dotenv()

    # Claves desde .env
    openai_api_key = os.getenv("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not openai_api_key:
        raise ValueError("No se encontró OPENAI_API_KEY en .env")
    if not tavily_api_key:
        raise ValueError("No se encontró TAVILY_API_KEY en .env")

    # Parámetros generales
    config = {
        "openai_api_key": openai_api_key,
        "tavily_api_key": tavily_api_key,
        "model_name": "gpt-4o-mini",      # ajustado a gpt-4o-mini
        "max_tokens": 2000,
        "temperature": 0.7
    }

    # 1. Inicializa el LLM de OpenAI usando el import actualizado
    llm = ChatOpenAI(
        model_name=config["model_name"],
        openai_api_key=openai_api_key,
        temperature=config["temperature"],
        max_tokens=config["max_tokens"]
    )

    # 2. Inicializa la herramienta de búsqueda Tavily
    tavily_tool = TavilySearchResults(api_key=tavily_api_key)
    tools = [tavily_tool]

    # 3. Obtiene el prompt ReAct desde LangChain Hub
    prompt = hub.pull("hwchase17/react")

    # 4. Crea el agente ReAct
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    # 5. Crea el ejecutor del agente
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    # 6. Añade el ejecutor del agente al config
    config["langchain_agent"] = agent_executor

    return config
