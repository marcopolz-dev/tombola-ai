from enum import Enum
from datapizza.tracing import ContextTracing
from ai_engine import AIEngine
from datapizza.agents import Agent


class AgentRoles(str, Enum):
    GAME_MASTER = 'GameMaster'
    CARD_GENERATOR = 'CardGenerator'
    ELFO = 'Elfo'
    GRINCH = 'Grinch'
    LADY = 'Lady'

class AgentTypes(str, Enum):
    BANCO = 'banco'
    PLAYER = 'player'
    UTILITY = 'utility'
    TOOL = 'tool'


class TombolaAgent:
    """
    Rappresenta un agente di gioco.
    """
    def __init__(self, agent, meta):
        self.agent = agent
        self.meta = meta
        self.id = meta['role_id']
        self.name = meta['name']
        self.model = meta['model']
        self.default_sys_prompt = self.agent.system_prompt


    def esegui(self, prompt, context_name="Esecuzione TombolaAgent"):
        """
        ..     
        """
        try:
            with ContextTracing().trace(context_name):
                response = self.agent.run(prompt)
                
        except Exception as e:
            print(f"Errore tracing: {e}")
            response = self.agent.run(prompt)

        return response.text


    def aggiorna_system_prompt(self, new_prompt):
        """
        Aggiorna il prompt di sistema e resetta la memoria dell'agente.
        """
        client = AIEngine.get_client(self.model)
        self.agent = Agent(
            name=self.id,
            client=client,
            system_prompt=new_prompt
        )

        #self.agent.system_prompt = new_prompt        
        print(f"✅ {self.name}: Nuova personalità caricata!")


    def resetta_system_prompt(self):
        """
        Reimposta il prompt di sistema (originale) dell'agente.
        """
        self.agent.system_prompt = self.default_sys_prompt
        
        print(f"🧠 {self.name}: Prompt ripristinato!")


    @property
    def is_banco(self):
        return self.meta['type'] == AgentTypes.BANCO

    @property
    def is_player(self):
        return self.meta['type'] == AgentRoles.PLAYER

    @property
    def is_tool(self):
        return self.meta['type'] == AgentRoles.TOOL

    @property
    def is_utility(self):
        return self.meta['type'] == AgentRoles.UTILITY

        