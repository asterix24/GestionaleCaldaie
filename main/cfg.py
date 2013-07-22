HOME_STD_VIEW = [
 'stato_verifica',
 'codice_impianto',
 'cognome',
 'nome',
 'via',
 'citta',
 'numero_cellulare',
 'numero_telefono',
 'mail',
 'stato_impianto',
 'marca_caldaia',
 'modello_caldaia',
 'combustibile',
 'tipo_caldaia',
 'data_installazione',
 'data_ultima_verifica',
 'prossima_verifica',
 'ultima_analisi_combustione',
 'prossima_analisi_combustione',
 'colore_bollino',
 'note_verifica',
]

ANAGRAFE_STD_VIEW = [
 'codice_impianto',
 'numero_rapporto',
 'cognome',
 'nome',
 'codice_fiscale',
 'via',
 'citta',
 'cap',
 'numero_cellulare',
 'numero_telefono',
 'mail',
 'stato_impianto',
 'marca_caldaia',
 'modello_caldaia',
 'matricola_caldaia',
 'potenza_caldaia',
 'combustibile',
 'tipo_caldaia',
 'data_installazione',
 'data_contratto',
 'tipo_verifica',
 'data_ultima_verifica',
 'prossima_verifica',
 'ultima_analisi_combustione',
 'prossima_analisi_combustione',
 'colore_bollino',
 'valore_bollino',
 'note_verifica',
 'data_intervento',
 'tipo_intervento',
]

ANAGRAFE_CLIENTE_STD_VIEW = [
 'cognome',
 'nome',
 'codice_fiscale',
 'via',
 'citta',
 'cap',
 'numero_cellulare',
 'numero_telefono',
 'mail',
]

ANAGRAFE_IMPIANTI_STD_VIEW = [
'stato_impianto',
'codice_impianto',
'marca_caldaia',
'modello_caldaia',
'matricola_caldaia',
'potenza_caldaia',
'tipo_caldaia',
'combustibile',
'anzianita_impianto',
'data_installazione',
'data_contratto'
]

ANAGRAFE_VERIFICA_STD_VIEW = [
'stato_verifica',
'data_verifica',
'tipo_verifica',
'numero_rapporto',
'analisi_combustione',
'prossima_verifica',
'prossima_analisi_combustione',
'codice_id',
'colore_bollino',
'numero_bollino',
'valore_bollino',
'costo_intervento',
'stato_pagamento',
'note_verifica',
]

ANAGRAFE_INTERVENTI_STD_VIEW = [
'data_intervento',
'tipo_intervento',
'note_intervento'
]

DB_DATA_FIELD = [
'data_verifica',
'data_installazione',
'data_contratto',
'prossima_verifica',
'prossima_analisi_combustione',
'data_ultima_verifica',
'ultima_analisi_combustione',
'prossima_analisi_combustione',
]

GROUP_FIELD_VIEW = {
'cognome'             : { "field":"main_cliente.cognome",               "order":"asc" },
'nome'                : { "field":"main_cliente.nome",                  "order":"asc" },
'codice_fiscale'      : { "field":"main_cliente.codice_fiscale",        "order":"asc" },
'via'                 : { "field":"main_cliente.via",                   "order":"asc" },
'citta'               : { "field":"main_cliente.citta",                 "order":"asc" },
'cap'                 : { "field":"main_cliente.cap",                   "order":"asc" },
'numero_cellulare'    : { "field":"main_cliente.numero_cellulare",      "order":"asc" },
'numero_telefono'     : { "field":"main_cliente.numero_telefono",       "order":"asc" },
'mail'                : { "field":"main_cliente.mail",                  "order":"asc" },

'codice_impianto'     : { "field":"main_impianto.codice_impianto",       "order":"asc" },
'stato_impianto'      : { "field":"main_impianto.stato_impianto",       "order":"asc" },
'marca_caldaia'       : { "field":"main_impianto.marca_caldaia",        "order":"asc" },
'modello_caldaia'     : { "field":"main_impianto.modello_caldaia",      "order":"asc" },
'matricola_caldaia'   : { "field":"main_impianto.matricola_caldaia",    "order":"asc" },
'potenza_caldaia'     : { "field":"main_impianto.potenza_caldaia",      "order":"asc" },
'combustibile'        : { "field":"main_impianto.combustibile",         "order":"asc" },
'tipo_caldaia'        : { "field":"main_impianto.tipo_caldaia",         "order":"asc" },
'data_installazione'  : { "field":"main_impianto.data_installazione",   "order":"asc" },
'data_contratto'      : { "field":"main_impianto.data_contratto",       "order":"asc" },
'anzianita_impianto'  : { "field":"main_impianto.anzianita_impianto",   "order":"asc" },

'stato_verifica'                : { "field":"main_verifica.stato_verifica",                "order":"asc"},
'data_verifica'                 : { "field":"main_verifica.data_verifica",                 "order":"asc"},
'tipo_verifica'                 : { "field":"main_verifica.tipo_verifica",                 "order":"asc"},
'altro_tipo_verifica'           : { "field":"main_verifica.altro_tipo_verifica",           "order":"asc"},
'codice_id'                     : { "field":"main_verifica.codice_id",                     "order":"asc"},
'numero_rapporto'               : { "field":"main_verifica.numero_rapporto",               "order":"asc"},
'prossima_verifica'             : { "field":"main_verifica.prossima_verifica",             "order":"asc"},
'analisi_combustione'           : { "field":"main_verifica.analisi_combustione",           "order":"asc"},
'colore_bollino'                : { "field":"main_verifica.colore_bollino",                 "order":"asc"},
'altro_colore_bollino'          : { "field":"main_verifica.altro_colore_bollino",           "order":"asc"},
'numero_bollino'                : { "field":"main_verifica.numero_bollino",                 "order":"asc"},
'valore_bollino'                : { "field":"main_verifica.valore_bollino",                 "order":"asc"},
'prossima_analisi_combustione'  : { "field":"main_verifica.prossima_analisi_combustione",   "order":"asc"},
'stato_pagamento'               : { "field":"main_verifica.stato_pagamento",                "order":"asc"},
'costo_intervento'              : { "field":"main_verifica.costo_intervento",               "order":"asc"},
'note_verifica'                 : { "field":"main_verifica.note_verifica",                  "order":"asc"},
'data_ultima_verifica'          : { "field":"main_verifica.data_ultima_verifica",           "order":"asc"},
'ultima_analisi_combustione'    : { "field":"main_verifica.ultima_analisi_combustione",     "order":"asc"},

'data_intervento'               : { "field":"main_intervento.data_intervento",     "order":"asc"},
'tipo_intervento'               : { "field":"main_intervento.tipo_intervento",     "order":"asc"},
'note_intervento'               : { "field":"main_intervento.note_intervento",     "order":"asc"},

}

DATA_FIELD_STR_FORMAT = "%d/%m/%Y"
BREADCRUMB = []

