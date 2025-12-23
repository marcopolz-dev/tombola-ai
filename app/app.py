import streamlit as st
import random
import time

from game_config import get_dettagli_numero
from game_logic import TombolaLogic
from agents_manager import AgentsManager
from agent import AgentRoles, AgentTypes
from ui import TombolaUI


# SETUP UI INIZIALE
TombolaUI.setup_page() # Configurazione pagina
TombolaUI.setup_app_title() # Titolo e descrizione
TombolaUI.render_sidebar() # controlli partita

# Layout a 3 colonne
col_game, col_chat, col_players = st.columns([1, 2, 1])

# Controllo se è necessario inizializzare
needs_initialization = 'initialized' not in st.session_state

if needs_initialization:
    # Reset stato di gioco
    st.session_state.agents = {} # Dizionario di agenti attivi
    #st.session_state.agents_meta = {}         
    st.session_state.numeri_estratti = []
    st.session_state.chat_history = []
    st.session_state.cartelle = {}
    st.session_state.player_ids = []
    st.session_state.banco_id = None
    st.session_state.vincite_registrate = {}
    st.session_state.auto_play = False
    st.session_state.tombola_fatta = False


@st.dialog("Modifica Personalità Agente")
def open_editor_agente(player_id, meta= None):

    player = st.session_state.agents[player_id]

    # Header dialog
    c_icon, c_tit = st.columns([1, 5], vertical_alignment="center")
    with c_icon:
        img_b64 = TombolaUI.get_img_as_base64(player.meta["icon"])
        st.markdown(f'<img src="data:image/png;base64,{img_b64}" class="banco-header-img">', unsafe_allow_html=True)

    with c_tit:
        st.write(f"Stai modificando di: **{player.name}**")
        if player.is_banco:
            st.caption("⚠️ Attenzione: Modificare il Banco influenza tutto il gioco!")

    # Recupera il prompt attuale dell'agente
    current_prompt = player.agent.system_prompt
    
    # Text Area
    new_prompt = st.text_area("System Prompt", value=current_prompt, height=300)
    
    # Spazio vuoto
    st.write("")
    
    # --- BOTTONI AZIONE ---
    col_save, col_reset = st.columns([1, 1])
    
    with col_save:
        # Bottone di save 
        if st.button("Salva Modifiche", type="primary", use_container_width=True):
            player.aggiorna_system_prompt(new_prompt)
            st.success("Personalità aggiornata!")
            time.sleep(0.8)
            st.rerun()
            
    with col_reset:
        # Bottone di reset 
        if st.button("Ripristina Originale", use_container_width=True):
            player.resetta_system_prompt()
            st.toast(f"{player.name} è tornato alle impostazioni di fabbrica!", icon="🏭")
            time.sleep(0.8)
            st.rerun()


#======================
# UI Colonna Tabellone
#=====================
with col_game:
    dashboard_ph = st.empty()
    banco_status_ph = st.empty()

    # Recupera i metadati del banco per il rendering
    current_banco_meta = None

    if st.session_state.banco_id:
        current_banco_meta = st.session_state.agents.get(st.session_state.banco_id).meta

    # Mostra il tabellone vuoto in fase di caricamento
    TombolaUI.render_dashboard(
        dashboard_ph, st.session_state.numeri_estratti, current_banco_meta,
        on_edit_callback=lambda: open_editor_agente(st.session_state.banco_id),
        key_suffix="main"
    )


#======================
# UI Colonna Chat
#=====================
with col_chat:
    st.subheader("Tavolo")
    chat_ph = st.empty()
    if not needs_initialization:
        TombolaUI.render_chat(chat_ph, st.session_state.chat_history, st.session_state.agents)
    else:
        st.info("In attesa dei giocatori...")


#======================
# UI Colonna Giocatori
#=====================
player_status_phs = {} # placeholder per ogni giocatore

with col_players:
    st.subheader("Giocatori")
    st.caption("Clicca ⚙️ per modificare l'AI")

    if needs_initialization:
        # Suggestione visiva di caricamento. L'utente sa che qualcosa sta succedendo.
        status_box = st.status("🎅 Convocazione Giocatori in corso...", expanded=True)

        with status_box:
            st.write("I giocatori si siedono al tavolo.")
            agents_dict = AgentsManager.initialize_agents()

            # Salviamo nello stato i dati degli agenti (player e banco)
            st.session_state.agents = agents_dict       
            #st.session_state.agents_meta = agents_meta
            st.session_state.banco_id = AgentsManager.get_banco_id(agents_dict)
            st.session_state.player_ids = AgentsManager.get_players_ids(agents_dict)

            agent_cardgen =  st.session_state.agents.get(AgentRoles.CARD_GENERATOR, None)
            
            st.write("Distribuzione delle cartelle in corso...")
            progress_bar = st.progress(0) # Barra di progresso per feedback visivo
            total_players = len(st.session_state.player_ids)
            
            for idx, player_id in enumerate(st.session_state.player_ids):
                c1, c2 = [], []
                # Generazione Cartelle, 2 per giocatore
                if agent_cardgen:
                    c1 = TombolaLogic.genera_cartella(agent_cardgen)
                    c2 = TombolaLogic.genera_cartella(agent_cardgen)
                    
                st.session_state.cartelle[player_id] = [c1, c2]
                st.session_state.vincite_registrate[player_id] = []
                
                # Aggiorna la barra progresso
                progress_bar.progress((idx + 1) / total_players)
            
            st.write("✨ Tutto pronto!")
            time.sleep(1) # Una pausa per far vedere il completamento
            
        st.session_state.initialized = True
        st.rerun() # Ricarica la pagina per mostrare i dati aggiornati
        
    else:
        # Renderizza i giocatori
        for player_id in st.session_state.player_ids:
            meta =  st.session_state.agents[player_id].meta #st.session_state.agents_meta[player_id]
            
            c_head, c_btn = st.columns([5, 1], vertical_alignment="center")

            with c_head:
                TombolaUI.render_player_header(meta)

            with c_btn:
                if st.button("⚙️", key=f"btn_edit_{player_id}", help=f"Modifica {meta['name']}", type="tertiary"):
                    open_editor_agente(player_id)

            #TombolaUI.render_player_header(meta)
            player_status_phs[player_id] = st.empty()
            TombolaUI.render_player_cartelle(st.session_state.cartelle[player_id], st.session_state.numeri_estratti)
            #st.divider()


# ======================
# TURNO DI GIOCO 
# =====================
def esegui_turno():

    # Controlla se la partita è finita    
    if len(st.session_state.numeri_estratti) >= 90:
        st.session_state.auto_play = False
        return

    banco_id = st.session_state.banco_id
    banco_agent = st.session_state.agents[banco_id]


    # Estrazione del numero e annuncio
    banco_status_ph.info(f"🎲 **{banco_agent.name}** sta pescando i numeri...")
    time.sleep(1.0)
    nuovo = random.randint(1, 90)
    while nuovo in st.session_state.numeri_estratti:
        nuovo = random.randint(1, 90)
    st.session_state.numeri_estratti.append(nuovo)

    TombolaUI.render_dashboard(
        dashboard_ph, st.session_state.numeri_estratti, banco_agent.meta, 
        on_edit_callback=lambda: open_editor_agente(banco_id) if banco_id else None,
        key_suffix="loop"
    )


    # ANNUNCIO DEL NUMERO
    banco_status_ph.warning(f"🎤 **{banco_agent.name}** consulta la Smorfia...")
    significato, napoletana, battuta = get_dettagli_numero(nuovo)
    prompt = f"Numero: {nuovo}, {significato}. Battuta: {battuta}. Annuncialo."
    msg = banco_agent.esegui(prompt, context_name="annuncio_banco")
    st.session_state.chat_history.append({"role": banco_id, "msg": msg})
    TombolaUI.render_chat(chat_ph, st.session_state.chat_history, st.session_state.agents)
    banco_status_ph.empty() 


    # VERIFICA DELLE VINCITE GIOCATORI
    eventi_turno = []

    # Contesto condiviso, contiene i messaggi recenti della chat
    shared_context = TombolaLogic.ultimi_messaggi_chat(st.session_state.chat_history, st.session_state.agents, limit=4)

    for pid in st.session_state.player_ids:
        # player_meta = st.session_state.agents_meta[pid] # Non usato qui ma utile
        player_agent = st.session_state.agents[pid]
        cartelle = st.session_state.cartelle[pid]
        
        player_status_phs[pid].info(f"👀 Controllo...")
        time.sleep(0.5) 
        
        status_msgs = []
        for c in cartelle:
            vincita = TombolaLogic.verifica_vincite(c, st.session_state.numeri_estratti)
            if vincita and vincita not in st.session_state.vincite_registrate[pid]:
                status_msgs.append(f"HO FATTO {vincita}!!!")
                st.session_state.vincite_registrate[pid].append(vincita)
                eventi_turno.append(f"{pid}: {vincita}")
                if vincita == "TOMBOLA": st.session_state.tombola_fatta = True
        
        if status_msgs or random.random() > 0.7:
            player_status_phs[pid].success(f"💬 Sta scrivendo...")

            info = f"""
            CONTESTO DELLA CHAT RECENTE (L'ordine è cronologico):
            {shared_context}
            ----------------
            EVENTO ATTUALE:
            È stato estratto il numero: {nuovo}.
            IL TUO STATO NEL GIOCO: {', '.join(status_msgs) if status_msgs else 'Niente'}.
            
            OBIETTIVO:
            Commenta l'estrazione o RISPONDI a quello che hanno detto gli altri personaggi nel contesto recente.
            Mantieni la tua personalità. Sii breve (max 15/20 parole). RISPONDI IN ITALIANO.
            """

            response = player_agent.esegui(info, context_name=f"messaggio_giocatore_{pid}")
            st.session_state.chat_history.append({"role": pid, "msg": response})
            
            # Aggiorniamo il contesto per il prossimo giocatore nel loop for
            shared_context += f"- {player_agent.name}: {response}\n"

            TombolaUI.render_chat(chat_ph, st.session_state.chat_history, st.session_state.agents)
        
        player_status_phs[pid].empty()


    # IL BANCO VERIFICA SE UN GIOCATOR HA VINTO
    if eventi_turno:
        banco_status_ph.error(f"🚨 Verifica vincite...")
        time.sleep(1.0)
        msg_check = banco_agent.esegui(f"Qualcuno ha urlato: {eventi_turno}. Conferma!", context_name="banco_annuncia_vincita")
        st.session_state.chat_history.append({"role": banco_id, "msg": msg_check})
        TombolaUI.render_chat(chat_ph, st.session_state.chat_history, st.session_state.agents)
        banco_status_ph.empty()
        if st.session_state.tombola_fatta:
            st.session_state.auto_play = False



# ======================
# GAME LOOP 
# =====================
if not needs_initialization:
    if st.session_state.tombola_fatta:
        banco_status_ph.success("🏆 PARTITA TERMINATA!")
        st.balloons() 
    elif st.session_state.auto_play:
        esegui_turno()
        for i in range(st.session_state.speed, 0, -1):
            banco_status_ph.info(f"⏳ Prossima estrazione: {i}")
            time.sleep(1)
        banco_status_ph.empty()
        st.rerun()
