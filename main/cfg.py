HOME_STD_VIEW = [
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
 'tipo_intervento',
 'data_intervento',
]

ANAGRAFE_CLIENTE_STD_VIEW = [
 'cognome',
 'nome',
 'codice_fiscale',
 'via',
 'citta',
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
'data_installazione',
'data_contratto'
]

ANAGRAFE_VERIFICA_STD_VIEW = [
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

GROUP_FIELD_VIEW = {
"cognome"            : { "field":"main_cliente.cognome",             "order":"asc" },
"nome"               : { "field":"main_cliente.nome",                "order":"asc" },
"via"                : { "field":"main_cliente.via",                 "order":"asc" },
"citta"              : { "field":"main_cliente.citta",               "order":"asc" },
"marca_caldaia"      : { "field":"main_impianto.marca_caldaia",      "order":"asc" },
"modello_caldaia"    : { "field":"main_impianto.modello_caldaia",    "order":"asc" },
"combustibile"       : { "field":"main_impianto.combustibile",       "order":"asc" },
"data_installazione" : { "field":"main_impianto.data_installazione", "order":"asc" },
"data_contratto"     : { "field":"main_impianto.data_contratto",     "order":"asc" },
"potenza_caldaia"    : { "field":"main_impianto.potenza_caladaia",   "order":"asc" },
"tipo_caldaia"       : { "field":"main_impianto.tipo_caldaia",       "order":"asc" },
}

