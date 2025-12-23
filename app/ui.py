import os
import streamlit as st
import base64

class TombolaUI:
    
    # Mappa dei colori utilizzati nei messaggi di chat
    CHAT_STYLES = {
        "success": {"bg": "#d4edda", "color": "#155724", "border": "#c3e6cb"}, # Verde
        "error":   {"bg": "#f8d7da", "color": "#721c24", "border": "#f5c6cb"}, # Rosso
        "warning": {"bg": "#fff3cd", "color": "#856404", "border": "#ffeeba"}, # Giallo
        "info":    {"bg": "#d1ecf1", "color": "#0c5460", "border": "#bee5eb"}, # Blu
    }


    @staticmethod
    def render_thin_divider():
        """Linea di separazione sottile con margini ridotti"""
        st.markdown("""
            <hr style='
                margin-top: 5px; 
                margin-bottom: 5px; 
                border: none; 
                border-top: 1px solid #444;
            '>
        """, unsafe_allow_html=True)


    @staticmethod
    def get_img_as_base64(file_path):
        """Converte una immagine locale in base64"""
        if not os.path.exists(file_path):
            return ""
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()


    @staticmethod
    def setup_page():
        st.set_page_config(page_title="Tombola AI", layout="wide")
        st.markdown("""
        <style>
            .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
            h1 { margin-top: 1rem !important; padding-bottom: 0.6rem !important; }
            
            .tombola-cell { width: 100%; height: 25px; text-align: center; line-height: 25px; 
                            border: 1px solid #ddd; border-radius: 3px; font-size: 12px; margin: 1px; }

            .banco-header-img {
                width: 50px; height: 50px; border-radius: 50%; 
                object-fit: cover; vertical-align: middle;
            }
        </style>
        """, unsafe_allow_html=True)


    @staticmethod
    def setup_app_title():
        #st.title("🎁 Xmas - Tombola tra Agenti AI 🎄 ")
        st.markdown("""
            <h1 style='font-size: 2.0rem;'>
                🎁 Xmas - Tombola tra Agenti AI 🎄
            </h1>
        """, unsafe_allow_html=True)
        TombolaUI.render_thin_divider()


    @staticmethod
    def render_sidebar():
        with st.sidebar:
            st.header("Partita")
            c1, c2 = st.columns(2)
            if c1.button("START", type="primary"): st.session_state.auto_play = True
            if c2.button("STOP"): st.session_state.auto_play = False
            
            status_emoji = ":)" if st.session_state.get('auto_play') else ":/"
            status_text = "LIVE" if st.session_state.get('auto_play') else "PAUSA"
            st.metric("Stato", f"{status_emoji} {status_text}")
            st.slider("Attesa (sec)", 1, 10, 5, key="speed")


    @staticmethod
    def render_dashboard(container, numeri_estratti, banco_meta=None, on_edit_callback=None, key_suffix=""):
        last_num = numeri_estratti[-1] if numeri_estratti else "-"
        
        with container.container():
            # 1. HEADER BANCO
            if banco_meta:
                #c_img, c_info = st.columns([1, 5])
                c_img, c_info, c_btn = st.columns([1, 5, 1], vertical_alignment="center")

                with c_img:
                    if banco_meta.get("icon"):
                        img_b64 = TombolaUI.get_img_as_base64(banco_meta["icon"])
                        st.markdown(f'<img src="data:image/png;base64,{img_b64}" class="banco-header-img">', unsafe_allow_html=True)
                    else:
                        st.markdown(f"## {banco_meta.get('emoji', '🎲')}")

                with c_info:
                    st.markdown(f"{banco_meta['name']}")
                    st.caption("Il **Banco** di questa partita")

                with c_btn:
                    if on_edit_callback:
                        if st.button("⚙️", key=f"btn_edit_banco_{key_suffix}", type="tertiary", help="Modifica personalità Banco"):
                            on_edit_callback()

                #st.divider()
                #TombolaUI.render_thin_divider()

            # NUMERO ESTRATTO
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.markdown(f"""
                <div style="text-align:center; background:#ff4b4b; color:white; border-radius:10px; padding:10px; margin-bottom:15px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                    <div style="font-size:0.8em; text-transform:uppercase; letter-spacing:1px;">Numero Estratto</div>
                    <div style="font-size:3em; font-weight:bold; line-height:1;">{last_num}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("##### Tabellone")
            
            # IL TABELLONE 
            html_content = "<div style='border: 2px solid #555; background: #fffbe6; padding: 10px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'>"
            html_content += "<div style='display:grid; grid-template-columns:repeat(10, 1fr); gap:4px;'>"
            
            for i in range(1, 91):
                if i in numeri_estratti:
                    # Stile numero uscito
                    style = "background:#d32f2f; color:#fff; border:1px solid #b71c1c; font-weight:bold; transform:scale(1.1); box-shadow:0 2px 4px rgba(0,0,0,0.2);"
                else:
                    # Stile numero vuoto
                    style = "background:rgba(255,255,255,0.4); color:#444; border:1px solid #ddd;"

                html_content += f"<div style='{style} border-radius:4px; text-align:center; padding:5px 0; font-size:12px; transition: all 0.3s ease;'>{i}</div>"
            
            html_content += "</div></div>"
            
            # Rendering del tabellone
            st.markdown(html_content, unsafe_allow_html=True)
            
            # Statistica
            progress = len(numeri_estratti) / 90
            st.caption(f"Numeri estratti: {len(numeri_estratti)} / 90")
            st.progress(progress)


    @staticmethod
    def render_chat(container, chat_history, agents):
        """
        Disegna la chat. Icona giocatore + messaggio.
        """
        with container.container(height=600):
            if not chat_history:
                st.info("La partita sta per iniziare...")
                
            for chat in reversed(chat_history[-20:]):
                role_id = chat['role']
                msg = chat['msg']
                meta = agents.get(role_id).meta if agents.get(role_id) else {"emoji": "❓", "ui_style": "info", "name": role_id}

                # Recuperiamo il colore assegnato al personaggio
                style = TombolaUI.CHAT_STYLES.get(meta['ui_style'], TombolaUI.CHAT_STYLES['info'])
                
                # Recuperiamo l'immagine del personaggio
                img_tag = ""
                if meta.get("icon"):
                    img_b64 = TombolaUI.get_img_as_base64(meta["icon"])
                    if img_b64:
                        img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width:35px; height:35px; border-radius:50%; object-fit:cover; border:0px solid rgba(0,0,0,0.1); margin-right:10px; flex-shrink:0;">'
                
                # Se non c'è immagine, usiamo l'emoji di default
                if not img_tag:
                     img_tag = f'<span style="font-size:25px; margin-right:10px;">{meta.get("emoji", "❓")}</span>'

                # BOX Messaggio
                html_box = f"""
                <div style="
                    background-color: {style['bg']};
                    color: {style['color']};
                    border: 1px solid {style['border']};
                    padding: 10px;
                    border-radius: 8px;
                    margin-bottom: 8px;
                    display: flex;
                    align-items: flex-start;
                ">
                    {img_tag}
                    <div>
                        <div style="font-weight:bold; font-size:0.9em; margin-bottom:2px;">{meta['name']}</div>
                        <div style="font-size:0.95em; line-height:1.4;">{msg}</div>
                    </div>
                </div>
                """
                
                st.markdown(html_box, unsafe_allow_html=True)


    @staticmethod
    def render_player_header(meta):
        """
        Colonna giocatori. Sezione header con icona e nome giocatore.
        """
        img_tag = ""
        if meta.get("icon"):
            img_b64 = TombolaUI.get_img_as_base64(meta["icon"])
            if img_b64:
                img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; border:0px solid #ddd; margin-right:10px;">'
            else:
                img_tag = f'<span style="font-size:30px; margin-right:10px;">{meta.get("emoji", "")}</span>'
        else:
            img_tag = f'<span style="font-size:30px; margin-right:10px;">{meta.get("emoji", "")}</span>'

        html = f"""
        <div style="display:flex; align-items:center; margin-bottom:10px; padding-top:10px;">
            {img_tag}
            <div style="font-size:1.3em; font-weight:bold; color:#f0f2f6;">{meta['name']}</div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)


    @staticmethod
    def render_player_cartelle(cartelle_list, numeri_estratti):
        for i, c in enumerate(cartelle_list):
            TombolaUI._render_player_cartella(c, numeri_estratti, f"Cartella #{i+1}")


    @staticmethod
    def _render_player_cartella(cartella, numeri_estratti, titolo):
        """
        Renderizza la cartella del giocatore con i numeri estratti evidenziati.
        """
        # Titolo
        st.markdown(f"<div style='margin-bottom:2px; font-size:0.7em; color:#888; margin-top:5px;'>{titolo}</div>", unsafe_allow_html=True)
        
        # Container esterno (Beige)
        html = "<div style='border:1px solid #555; background:#fffbe6; padding:5px; border-radius:6px; margin-bottom:8px; box-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>"
        
        for riga in cartella:
            # Grid Riga
            html += "<div style='display:grid; grid-template-columns:repeat(9, 1fr); gap:3px; margin-bottom:3px;'>"
            for num in riga:
                if num == 0:
                    # Casella Vuota
                    html += "<div style='height:24px; border:1px solid #e0e0e0; background:rgba(0,0,0,0.03); border-radius:3px;'></div>"
                else:
                    # Casella Numero
                    if num in numeri_estratti:
                        # STILE ROSSO (Uscito)
                        style = "background:#d32f2f; color:#fff; border:1px solid #b71c1c; font-weight:bold; transform:scale(1.05); box-shadow:0 1px 3px rgba(0,0,0,0.3);"
                    else:
                        # STILE BEIGE (Normale)
                        style = "background:rgba(255,255,255,0.6); color:#333; border:1px solid #dcdcdc;"
                    
                    # Div del numero
                    html += f"<div style='{style} border-radius:3px; text-align:center; height:24px; line-height:24px; font-size:11px; cursor:default; transition: all 0.3s ease;'>{num}</div>"
            
            html += "</div>" 
            
        html += "</div>" 
        
        st.markdown(html, unsafe_allow_html=True)