import os
from datapizza.clients.openai_like import OpenAILikeClient

class AIEngine:
    """ 
    Questa classe gestisce il ciclo di vita del client AI.
    """
    @staticmethod
    def get_client(model_name: str):
        """ 
        Restituisce un'istanza del client AI configurata con il modello specificato.
        """      
        client = OpenAILikeClient(
            model=model_name, 
            api_key=os.getenv("OPENAI_API_KEY", "ollama-key"),
            base_url=os.getenv("OPENAI_BASE_URL", "http://ollama:11434")
        )
        print(f"[AIEngine] Nuovo client: {model_name}")
        return client
