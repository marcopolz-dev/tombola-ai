# game_logic.py
import random
import json
import re

from datapizza.tracing import ContextTracing

class TombolaLogic:
    
    @staticmethod
    def genera_cartella(cardgen_agent):
        """
        Genera i numeri con l'AI, ma usa il codice per posizionarli nelle colonne corrette.
        """
        print("L'agente matematico sta provando a generare una cartella...")
        try:
            response = cardgen_agent.esegui("Genera una nuova cartella valida adesso.", context_name="genera_cartella")
            text = response.strip()
            
            match = re.search(r'\[\[.*\]\]', text, re.DOTALL)
            if match: text = match.group(0)
            
            cartella_raw = json.loads(text)
            
            # Filtra tutti i numeri > 0 generati dall'AI (ignoriamo la posizione errata)
            numeri_trovati = []
            for riga in cartella_raw:
                for n in riga:
                    if isinstance(n, int) and 1 <= n <= 90:
                        numeri_trovati.append(n)
            
            # Rimuove i duplicati e ordina
            numeri_unici = sorted(list(set(numeri_trovati)))
            
            # Se l'AI ha generato pochi numeri, fallback
            if len(numeri_unici) < 15: 
                raise ValueError(f"L'agente matematico ha generato solo {len(numeri_unici)} numeri validi")
                
            # Ricostruiamo la cartella posizionando i numeri nelle colonne giuste
            numeri_da_usare = numeri_unici[:15] # Prendiamo i primi 15
            nuova_cartella = [[0]*9 for _ in range(3)]
            
            # Distribuzione intelligente
            rows_count = [0, 0, 0] # Contatore numeri per riga
            
            for n in numeri_da_usare:
                # Calcola colonna corretta (es. 5 -> col 0, 15 -> col 1, 90 -> col 8)
                col = 8 if n == 90 else n // 10
                
                # Cerca una riga libera in quella colonna
                piazzato = False
                for r in range(3):
                    # Regola: cella vuota E la riga ha meno di 5 numeri
                    if nuova_cartella[r][col] == 0 and rows_count[r] < 5:
                        nuova_cartella[r][col] = n
                        rows_count[r] += 1
                        piazzato = True
                        break
                            
            return nuova_cartella

        except Exception as e:
            print(f"⚠️ L'Agente matematico ha fallito/generato dati sporchi ({e}).")
            return [] 

    @staticmethod
    def verifica_vincite(cartella, numeri_estratti):
        """Controlla se la cartella ha fatto Ambo, Terna, ecc."""
        max_punti_riga = 0
        tombola_counter = 0
        numeri_cartella_pieni = 0
        
        for riga in cartella:
            punti_riga = 0
            for num in riga:
                if num != 0:
                    numeri_cartella_pieni += 1
                    if num in numeri_estratti:
                        punti_riga += 1
                        tombola_counter += 1
            if punti_riga > max_punti_riga:
                max_punti_riga = punti_riga
                
        vincita = None
        if max_punti_riga == 2: vincita = "AMBO"
        elif max_punti_riga == 3: vincita = "TERNA"
        elif max_punti_riga == 4: vincita = "QUATERNA"
        elif max_punti_riga == 5: vincita = "CINQUINA"
        
        if tombola_counter == numeri_cartella_pieni:
            vincita = "TOMBOLA"
            
        return vincita

    @staticmethod
    def ultimi_messaggi_chat(history, agents, limit=5):
        """
        Recupera gli ultimi 'limit' messaggi e li formatta come stringa per il prompt.
        Es:
        Grinch: Che schifo questo numero!
        Elfo: Ma no, è bellissimo!
        """
        if not history:
            return "Nessuna conversazione precedente."
        
        context_str = ""
        # Gli ultimi N messaggi
        recent_msgs = history[-limit:]
        
        for msg in recent_msgs:
            role_id = msg['role']
            # Nome reale dell'agente dai metadati
            agent_name = agents[role_id].name if role_id in agents else role_id
            text = msg['msg']
            context_str += f"- {agent_name}: {text}\n"
        
        return context_str
