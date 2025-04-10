import os
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults

def cargar_configuracion():
    """Carga las variables de entorno y configura los componentes principales"""
    load_dotenv()
    
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "tavily_api_key": os.getenv("TAVILY_API_KEY"),
        "model_name": "gpt-4",
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    return config