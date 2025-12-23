###############################################################
# Prompt, Configurazioni e Dizionari                       
#
###############################################################


# PROMPT per le regole generali del gioco
REGOLE_GIOCO = """
SEI IN UNA SIMULAZIONE DI TOMBOLA.
PARLA SOLO IN ITALIANO CORRETTO E NATURALE.
NON RIPETERE LE REGOLE DEL GIOCO.
SII BREVE (massimo 15-20 parole).
REGOLE DEL GIOCO:
1. Si estraggono numeri da 1 a 90.
2. Obiettivi di vincita in ordine:
   - AMBO: 2 numeri sulla stessa riga.
   - TERNA: 3 numeri sulla stessa riga.
   - QUATERNA: 4 numeri sulla stessa riga.
   - CINQUINA: 5 numeri sulla stessa riga.
   - TOMBOLA: Tutti i numeri della cartella coperti.
"""

# PROMPT di istruzioni del Banco. 
# Vengono assegnate al giocatore di turno, scelto per essere il Banco.
ISTRUZIONI_RUOLO_BANCO = """
==========================================================
🛑 ATTENZIONE: SEI STATO SELEZIONATO PER FARE IL BANCO! 🛑
MANTIENI LA TUA PERSONALITÀ (Grinch, Lady, Elfo, ecc.), ma ora hai nuovi compiti:

1. NON giochi più come concorrente. Il tuo compito è ESTRARRE i numeri.
2. Ti verrà fornito il numero estratto, il significato e una battuta.
3. ANNUNCIA il numero usando il tuo stile (es. se sei il Grinch, fallo con fastidio).
4. Se qualcuno vince, commenta la vincita con la tua personalità.
5. PARLI IN ITALIANO.
6. NON dire "Sono il banco", comportati come tale.
==========================================================
"""


# Dizionario - formato: Numero: ("Significato Classico", "Smorfia Napoletana", "Commento Natalizio/Divertente")
# La fonte dei significati è la tradizione della Smorfia, da Wikipedia https://it.wikipedia.org/wiki/La_smorfia.
# Per il contesto natalizio, sono stati aggiunti commenti divertenti a tema generati da una AI.
SMORFIA_NATALIZIA = {
    1: ("L'Italia", "L'Italia", "Tutti a tavola per il cenone, da Nord a Sud!"),
    2: ("La bambina", "'A criatura", "Piccola come il Bambinello nel presepe!"),
    3: ("La gatta", "'A gatta", "Ha appena fatto cadere l'albero di Natale!"),
    4: ("Il maiale", "'O puorco", "Il protagonista del secondo piatto!"),
    5: ("La mano", "'A mano", "La mano che scarta i regali."),
    6: ("Quella che guarda a terra", "Chella che guarda 'nterra", "Cerca la lenticchia caduta per i soldi!"),
    7: ("Il vaso", "'O vasetto", "Pieno di miele per gli struffoli!"),
    8: ("La Madonna", "'A Madonna", "Oggi è l'Immacolata, si frigge!"),
    9: ("La figliolanza", "'A figliata", "Quanti parenti siamo a tavola?!"),
    10: ("I fagioli", "'E fasule", "Non mangiateli! Servono per segnare i numeri!"),
    11: ("I topolini", "'E suricille", "Hanno rosicchiato i regali sotto l'albero!"),
    12: ("I soldati", "'E surdate", "A guardia del panettone!"),
    13: ("Sant'Antonio", "Sant'Antonio", "Proteggici dal mal di pancia per il troppo cibo!"),
    14: ("L'ubriaco", "'O mbriaco", "Lo zio che ha esagerato col vino rosso!"),
    15: ("Il ragazzo", "'O guaglione", "Che non vuole mettere il maglione della nonna!"),
    16: ("Il sedere", "'O culo", "Quello che serve per vincere stasera!"),
    17: ("La disgrazia", "'A disgrazia", "Aver finito il vino a metà cena!"),
    18: ("Il sangue", "'O sango", "Rosso come il vestito di Babbo Natale."),
    19: ("La risata", "'A resata", "Quella che ci facciamo se il Banco perde!"),
    20: ("La festa", "'A festa", "Luci, regali, cibo e tombola!"),
    21: ("La donna nuda", "'A femmena annura", "Copriti che fa freddo fuori!"),
    22: ("Il pazzo", "'O pazzo", "Chi spende tutto lo stipendio in regali!"),
    23: ("Lo scemo", "'O scemo", "Chi crede ancora che la dieta inizi a Natale!"),
    24: ("Le guardie", "'E guardie", "Controllano chi bara con i fagioli!"),
    25: ("Natale", "Natale", "È nato! Auguri a tutti, belli e brutti!"),
    26: ("La piccola Anna", "Nanninella", "Come la nonna che frigge le zeppole!"),
    27: ("Il vaso da notte", "'O cantero", "Troppa acqua e spumante, scappo in bagno!"),
    28: ("I seni", "'E zizz", "L'abbondanza sulla tavola imbandita!"),
    29: ("Il padre dei bimbi", "'O pate d' 'e criature", "Babbo Natale o papà che paga tutto?"),
    30: ("Le palle del tenente", "'E palle d' 'o tenente", "Le palline colorate che abbiamo appeso!"),
    31: ("Il padrone di casa", "'O padrone 'e casa", "Chi ospita il cenone e lava i piatti!"),
    32: ("Il capitone", "'O capitone", "Poverino, fritto e mangiato!"),
    33: ("Gli anni di Cristo", "L'anne 'e Cristo", "Un numero sacro, portate rispetto!"),
    34: ("La testa", "'A capa", "Il mal di testa dopo il pranzo di Natale!"),
    35: ("L'uccellino", "L'aucielluzzo", "Canta 'Tu scendi dalle stelle'!"),
    36: ("Le nacchere", "'E castagnelle", "Le castagne arrosto sul fuoco!"),
    37: ("Il monaco", "'O monaco", "Chi fa finta di digiunare aspettando il dolce."),
    38: ("Le botte", "'E mazzate", "Quelle che ci diamo per l'ultimo pezzo di torrone!"),
    39: ("La corda al collo", "'A funa 'n ganna", "La cravatta che mi soffoca al pranzo!"),
    40: ("L'ernia", "'A paposcia", "Lo sforzo per sollevare i cesti regalo!"),
    41: ("Il coltello", "'O curtiello", "Affilato per tagliare il panettone!"),
    42: ("Il caffè", "'O café", "Sveglia! Ne serve uno forte dopo il pranzo!"),
    43: ("La donna al balcone", "'Onna pereta", "La zia che spettegola sui vicini."),
    44: ("Le carceri", "'E ccancelle", "Siamo prigionieri a tavola fino a stasera!"),
    45: ("Il buon vino", "'O vino buono", "Cin cin! Un brindisi alla salute!"),
    46: ("I soldi", "'E denare", "I soldi che spero di vincere alla tombola!"),
    47: ("Il morto", "'O muorto", "Come mi sento dopo aver mangiato l'arrosto!"),
    48: ("Il morto che parla", "'O muorto che parla", "Lo zio che racconta sempre le stesse storie!"),
    49: ("Il pezzo di carne", "'O piezz' 'e carne", "L'arrosto che profuma tutta la casa!"),
    50: ("Il pane", "'O pane", "Meglio il panettone o il pandoro?"),
    51: ("Il giardino", "'O giardino", "Dove prendiamo il muschio per il presepe!"),
    52: ("La mamma", "'A mamma", "Mamma è sempre mamma, anche a Natale!"),
    53: ("Il vecchio", "'O viecchio", "Babbo Natale si fa vecchio, ma porta i doni!"),
    54: ("Il cappello", "'O cappello", "Quello rosso col pon-pon bianco!"),
    55: ("La musica", "'A musica", "Zampognari, suonate forte!"),
    56: ("La caduta", "'A caruta", "Attenti a non scivolare sul ghiaccio!"),
    57: ("Il gobbo", "'O scartellato", "Il gobbetto porta fortuna, toccatelo!"),
    58: ("Il pacco", "'O paccotto", "Il regalo riciclato dall'anno scorso!"),
    59: ("I peli", "'E pule", "La barba bianca di Babbo Natale!"),
    60: ("Il lamento", "'O lamiento", "Chi si lamenta che non vince mai un ambo!"),
    61: ("Il cacciatore", "'O cacciatore", "A caccia dell'ultimo regalo nei negozi!"),
    62: ("Il morto ammazzato", "'O muorto acciso", "Ucciso dalle troppe calorie!"),
    63: ("La sposa", "'A sposa", "Vestita di rosso per le feste!"),
    64: ("La marsina", "'A sciammeria", "Il cappotto elegante per la messa!"),
    65: ("Il pianto", "'O chianto", "Chi piange perché gli manca un solo numero!"),
    66: ("Le due zitelle", "'E ddoie zitelle", "Le zie che chiedono: 'e il fidanzatino?'"),
    67: ("Il totano nella chitarra", "'O totaro int' 'a chitarra", "Il pesce fresco della vigilia!"),
    68: ("La zuppa cotta", "'A zuppa cotta", "La minestra maritata, che bontà!"),
    69: ("Sottosopra", "Sott'e 'ncoppa", "Il caos dei pacchetti scartati!"),
    70: ("Il palazzo", "'O palazzo", "Tutto illuminato a festa!"),
    71: ("L'uomo di m...", "L'ommo 'e merda", "Chi regala i calzini bucati!"),
    72: ("Lo stupore", "'A meraviglia", "La faccia dei bimbi davanti ai regali!"),
    73: ("L'ospedale", "'O spitale", "Dove finiamo se mangiamo un altro dolce!"),
    74: ("La grotta", "'A rotta", "La grotta del presepe col bue e l'asinello!"),
    75: ("Pulcinella", "Pulecenella", "La maschera che porta allegria!"),
    76: ("La fontana", "'A funtana", "L'acqua che diventa vino stasera!"),
    77: ("I diavoli", "'E diavule", "Le tentazioni dei dolci a cui non resisto!"),
    78: ("La bella figliola", "'A bella figliola", "Bella come la Stella Cometa!"),
    79: ("Il ladro", "'O mariuolo", "Chi ruba i fagioli dal tabellone degli altri!"),
    80: ("La bocca", "'A vocca", "Piena di struffoli e roccocò!"),
    81: ("I fiori", "'E sciure", "Le Stelle di Natale rosse rosse!"),
    82: ("La tavola imbandita", "'A tavula 'mbandita", "Non c'è spazio nemmeno per i bicchieri!"),
    83: ("Il maltempo", "'O maletiempo", "Fuori piove o nevica, ma dentro si gioca!"),
    84: ("La chiesa", "'A cchiesa", "Tutti alla messa di mezzanotte!"),
    85: ("Le anime del Purgatorio", "'E l'anime d' 'o priatorio", "Anime sante, fateci fare ambo!"),
    86: ("Il negozio", "'A puteca", "Negozi pieni per gli ultimi acquisti!"),
    87: ("I pidocchi", "'E perucchie", "I fastidi che non vogliamo oggi!"),
    88: ("I caciocavalli", "'E caciocavalle", "Buoni con la marmellata o il miele!"),
    89: ("La vecchia", "'A vecchia", "La Befana che vien di notte!"),
    90: ("La paura", "'A paura", "Paura che i parenti non se ne vadano più!")
}


# Risolve i dettagli relativi al numero estratto nel formato previsto dal dizionario SMORFIA_NATALIZIA
#
def get_dettagli_numero(num):
    """Restituisce significato e commento/battuta."""
    val = SMORFIA_NATALIZIA.get(num, ("Numero Fortunato", "Speriamo porti bene!"))

    if isinstance(val, str):
        return val, "Un numero classico della tradizione!"
    return val
