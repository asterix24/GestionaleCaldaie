#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import decimal
import string

from django.db.models import Q
from django.forms.models import model_to_dict
from django.db import connection, transaction

from models import Cliente
from tools import *


FILTER_MODE_START =     '__istartswith'
FILTER_MODE_EXACT =     '__iexact'
FILTER_MODE_CONTAIN =  '__icontains'
FILTER_SHORT_ASCEN =   0
FILTER_SHORT_DESCEND = 1

def filter_records(ctx, key, value, mode = FILTER_MODE_CONTAIN):
    return ctx.filter(**{ key + mode : value })

def filter_dataInstallazione(ctx, start_y, start_m = None, start_d = None, stop_y = None, stop_m = None, stop_d = None):
    if stop_y is not None and stop_m is not None and stop_d is not None:
            return ctx.filter(data_installazione__range = (datetime.date(start_y, start_m, start_d),datetime.date(stop_y, stop_m, stop_d)))
    if start_m is not None:
            return ctx.filter(data_installazione__year = start_y).filter(data_installazione__month = start_m)
    else:
            return ctx.filter(data_installazione__year = start_y)

def filter_dataContratto(ctx, start_y, start_m = None, start_d = None, stop_y = None, stop_m = None, stop_d = None):
    if stop_y is not None and stop_m is not None and stop_d is not None:
            return ctx.filter(data_contratto__range = (datetime.date(start_y, start_m, start_d),datetime.date(stop_y, stop_m, stop_d)))
    if start_m is not None:
            return ctx.filter(data_contratto__year = start_y).filter(data_installazione__month = start_m)
    else:
            return ctx.filter(data_contratto__year = start_y)

def clienti_displayAll(ctx):
    return ctx.all()

def select_record(ctx, id):
    return ctx.get(pk=id)

def delete_record(ctx, id):
    return ctx.objects.get(pk=id).delete()

def insert_cliente(r):
    node = Cliente(**r)
#       dump(r)
    node.save()
    return node


ETICHETTE_ID = ['cliente_id', 'impianto_id', 'verifiche_id', 'intervento_id' ]

DB_SELECT_ALL = "\
SELECT * FROM main_cliente \
LEFT JOIN main_impianto ON main_impianto.cliente_impianto_id = main_cliente.id \
LEFT JOIN main_verifichemanutenzione ON main_verifichemanutenzione.verifiche_impianto_id = main_impianto.id \
LEFT JOIN main_intervento ON main_intervento.intervento_impianto_id = main_impianto.id \
"

#LEFT JOIN main_intervento ON main_intervento.intervento_impianto_id = main_impianto.id

DB_WHERE_MAIN_CLIENTE = "(\
main_cliente.numero_cellulare ILIKE %s OR \
main_cliente.via ILIKE %s OR \
main_cliente.nome ILIKE %s OR \
main_cliente.cognome ILIKE %s OR \
main_cliente.codice_fiscale ILIKE %s OR \
CAST(main_cliente.cliente_data_inserimento AS TEXT) ILIKE %s OR \
main_cliente.numero_telefono ILIKE %s OR \
main_cliente.mail ILIKE %s OR \
main_cliente.citta ILIKE %s OR \
main_impianto.modello_caldaia ILIKE %s OR \
CAST(main_impianto.impianto_data_inserimento AS TEXT) ILIKE %s OR \
main_impianto.matricola_caldaia ILIKE %s OR \
main_impianto.combustibile ILIKE %s OR \
CAST(main_impianto.data_installazione AS TEXT) ILIKE %s OR \
CAST(main_impianto.data_contratto AS TEXT) ILIKE %s OR \
CAST(main_impianto.data_prossima_verifica AS TEXT) ILIKE %s OR \
CAST(main_impianto.data_ultima_verifica AS TEXT) ILIKE %s OR \
main_impianto.tipo_caldaia ILIKE %s OR \
main_impianto.potenza_caldaia ILIKE %s OR \
CAST(main_impianto.data_ultima_analisi_combustione AS TEXT) ILIKE %s OR \
main_impianto.marca_caldaia ILIKE %s OR \
main_impianto.codice_impianto ILIKE %s OR \
CAST(main_impianto.data_prossima_analisi_combustione AS TEXT) ILIKE %s OR \
main_intervento.note_intervento ILIKE %s OR \
main_intervento.tipo_intervento ILIKE %s OR \
CAST(main_intervento.data_intervento AS TEXT) ILIKE %s OR \
CAST(main_verifichemanutenzione.data_scadenza AS TEXT) ILIKE %s OR \
main_verifichemanutenzione.note_verifiche_manutenzione ILIKE %s OR \
main_verifichemanutenzione.tipo_verifica_manutenzione ILIKE %s OR \
main_verifichemanutenzione.colore_bollino ILIKE %s OR \
CAST(main_verifichemanutenzione.data_verifica_manutenzione AS TEXT) ILIKE %s OR \
CAST(main_verifichemanutenzione.numero_bollino AS TEXT) ILIKE %s OR \
CAST(main_verifichemanutenzione.scadenza AS TEXT) ILIKE %s OR \
CAST(main_verifichemanutenzione.numero_rapporto AS TEXT) ILIKE %s )"


DB_ORDER = "ORDER BY main_cliente.cognome ASC, main_cliente.nome ASC"

def search_runQuery(query_str, param):
    cursor = connection.cursor()
    cursor.execute(query_str, param)

    desc = cursor.description
    l = []
    i = 0
    for col in desc:
            c = col[0]
            if c == 'id':
                    c = ETICHETTE_ID[i]
                    i += 1

            l.append(c)
    return [ dict(zip(l, row))
            for row in cursor.fetchall() ]

def search_clienteId(id):
    query_str = DB_SELECT_ALL + " WHERE main_cliente.id = %s " + DB_ORDER
    return search_runQuery(query_str, [id])

def search_impiantoId(id):
    query_str = DB_SELECT_ALL + " WHERE main_impianto.id = %s " + DB_ORDER
    return search_runQuery(query_str, [id])

def search_verificheId(id):
    query_str = DB_SELECT_ALL + " WHERE main_verifichemanutenzione.id = %s " + DB_ORDER
    return search_runQuery(query_str, [id])

def search_interventoId(id):
    query_str = DB_SELECT_ALL + " WHERE main_intervento.id = %s " + DB_ORDER
    return search_runQuery(query_str, [id])

def search_fullText(s):
    search_key = []
    if " " in s:
        search_key = s.strip().split(" ")
    else:
        search_key.append(s.strip())

    query_str = DB_SELECT_ALL
    query_str += " WHERE ( "
    param = []
    for i, key in enumerate(search_key):
        if len(key) >= 3:
            key = "%" + key + "%"
        else:
            key = key + "%"

        query_str += DB_WHERE_MAIN_CLIENTE
        param += [key] * DB_WHERE_MAIN_CLIENTE.count("%s")

        if (i == 0 and len(search_key) > 1) or i < len(search_key) - 1:
            query_str += " AND "

    query_str += " ) " + DB_ORDER

    return search_runQuery(query_str, param)
