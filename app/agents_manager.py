import yaml
import os
import random 
import game_config

from datapizza.agents import Agent
from datapizza.tracing import ContextTracing
from datapizza.tools import tool


from ai_engine import AIEngine
from agent import TombolaAgent, AgentRoles, AgentTypes


@tool
def tool_estrai_banco(nomi_candidati: str) -> str:
    """ Effettua il sorteggio tra i nomi dei candidati passati come stringa separata da virgole.
        Restituisce il nome del vincitore.
    """
    lista = [n.strip() for n in nomi_candidati.split(',') if n.strip()]
    
    if not lista:
        return "Nessun candidato valido fornito per il sorteggio."

    # Sorteggio    
    vincitore = random.choice(lista)
    
    print(f"🔧[TOOL] Sorteggio effettuato tra {lista} -> Vince: {vincitore}")
    return vincitore


class AgentsManager:
    """ Questa classe gestisce il caricamento, l'inizializzazione e la gestione degli agenti di gioco.
        Utilizza il file di configurazione agents.yaml per definire i dettagli degli agenti.
    """
    @staticmethod
    def _load_config():
        if not os.path.exists("agents.yaml"):
            raise FileNotFoundError("Il file agents.yaml non è stato trovato!")
            
        with open("agents.yaml", "r", encoding="utf-8") as file:
            agents_cfg = yaml.safe_load(file)
            
        # Aggiungiamo le regole di gioco al system prompt di tutti gli agenti
        for agent in agents_cfg:
            if "{{REGOLE_GIOCO}}" in agent["sys_prompt"]:
                agent["sys_prompt"] = agent["sys_prompt"].replace("{{REGOLE_GIOCO}}", game_config.REGOLE_GIOCO)
                   
        return agents_cfg


    @staticmethod
    def initialize_agents():
        """ Inizializza tutti gli agenti e restituisce un dizionario di agenti attivi 
            e un dizionario di metadati degli agenti.
        """    
        agents_config = AgentsManager._load_config()
        print("[AgentsManager] Definizione degli agenti caricata!")

        active_agents = {}

        if agents_config:

            # Instanziamo tutti gli agenti
            for conf in agents_config:
                role_id = conf.get("role_id", None)
                model_name = conf.get("model", None)
                if role_id is not None and model_name is not None:
                    agent = Agent(
                        name = role_id,
                        client = AIEngine.get_client(model_name),
                        system_prompt=conf.get("sys_prompt", "Sei un agente esperto e collaborativo."),
                        tools = [tool_estrai_banco] if role_id == "GameMaster" else [],
                        planning_interval=conf.get("planning_interval", 0)
                    ) 
                    # Dizionario di agenti attivi
                    active_agents[role_id] = TombolaAgent(agent, conf)

            print(f"[AgentsManager] Agenti attivi: { active_agents.keys() }")

            players = [
                agent for agent in active_agents.values() 
                if agent.meta.get("type") == AgentTypes.PLAYER
            ]

            print(f"[AgentsManager] Agenti giocatori attivi: {len(players)}")

            # Assegniamo il ruolo del BANCO
            if players:
                name_of_canditates = [
                    agent.name for agent in players
                ]
                name_of_canditates_str = ", ".join(name_of_canditates)
                print(f"[AgentsManager] Candidati al ruolo di {AgentTypes.BANCO.value}: {name_of_canditates_str}")

                agent_gm = AgentsManager.get_gamemaster(active_agents)

                print(f"⚖️ {agent_gm.name} sta scegliendo il Banco tra: {name_of_canditates_str}...")
                prompt = f"I candidati per il ruolo di Banco sono: {name_of_canditates_str}."

                try:
                    risposta_gm = agent_gm.esegui(prompt, context_name="Sorteggio ruolo Banco")
                    print(f"📢 Annuncio GM: {risposta_gm}")
                except Exception as e:
                    print(f"⚠️ Errore GM: {e}")
                    risposta_gm = ""

                banco_trovato = False
                if risposta_gm:
                    for player in players:
                        # Controlliamo se il nome del giocatore è nella risposta dell'AI
                        if player.name in risposta_gm:
                            player.meta['type'] = AgentTypes.BANCO
                            player.default_sys_prompt += game_config.ISTRUZIONI_RUOLO_BANCO
                            player.agent.system_prompt = player.default_sys_prompt
                            print(f"✅ [AgentsManager] AI. Ruolo BANCO assegnato a: {player.name}")
                            banco_trovato = True
                            break

                if not banco_trovato:
                    print("⚠️ [Fallback] Scelta casuale algoritmica per il Banco.")
                    role_id = random.choice(name_of_canditates) 
                    player = active_agents.get(role_id)                    
                    player.meta['type'] = AgentTypes.BANCO
                    player.default_sys_prompt += game_config.ISTRUZIONI_RUOLO_BANCO
                    player.agent.system_prompt = player.default_sys_prompt
                    print(f"✅ [AgentsManager] Fallback. Ruolo BANCO assegnato a: {player.name}")

            else:
                print("[AgentsManager] Nessun agente giocatore attivo trovato. Impossibile procedere.")
            
        return active_agents



    @staticmethod
    def get_banco_id(active_agents):
        """ Restituisce l'ID dell'agente di tipo "banco"."""
        for playerID, agent_obj in active_agents.items():
            if agent_obj.meta["type"] == AgentTypes.BANCO:
                return playerID
        return None

    @staticmethod
    def get_players_ids(active_agents):
        """ Restituisce la lista degli ID degli agenti di tipo "player"."""
        return [
            playerID for playerID, agent_obj in active_agents.items() 
            if agent_obj.meta["type"] == AgentTypes.PLAYER
        ]


    @staticmethod
    def get_gamemaster(active_agents):
        """Restituisce l'agente temporaneo che fa il sorteggio."""
        return AgentsManager.get_agent(AgentRoles.GAME_MASTER, active_agents)


    @staticmethod
    def get_agent(role_id, active_agents):
        """Restituisce l'agente temporaneo che fa il sorteggio."""
        return active_agents.get(role_id, None)

