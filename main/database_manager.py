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

import logging
logger = logging.getLogger(__name__)

#SELECT
DB_COLUM = """
main_cliente.numero_cellulare,
main_cliente.via,
main_cliente.nome,
main_cliente.cognome,
main_cliente.codice_fiscale,
main_cliente.cliente_data_inserimento,
main_cliente.numero_telefono,
main_cliente.mail,
main_cliente.citta,
main_cliente.id AS cliente_id,
main_impianto.modello_caldaia,
main_impianto.impianto_data_inserimento,
main_impianto.matricola_caldaia,
main_impianto.combustibile,
main_impianto.data_installazione,
main_impianto.data_contratto,
main_impianto.tipo_caldaia,
main_impianto.altro_tipo_caldaia,
main_impianto.potenza_caldaia,
main_impianto.altra_potenza_caldaia,
main_impianto.marca_caldaia,
main_impianto.codice_impianto,
main_impianto.id AS impianto_id,
main_intervento.note_intervento,
main_intervento.tipo_intervento,
main_intervento.data_intervento,
main_intervento.id AS intervento_id,
main_verifica.id AS verifica_id,
main_verifica.stato_verifica,
main_verifica.data_verifica,
main_verifica.tipo_verifica,
main_verifica.altro_tipo_verifica,
main_verifica.codice_id,
main_verifica.numero_rapporto,
main_verifica.prossima_verifica,
main_verifica.colore_bollino,
main_verifica.numero_bollino,
main_verifica.valore_bollino,
main_verifica.analisi_combustione,
main_verifica.prossima_analisi_combustione,
main_verifica.stato_pagamento,
main_verifica.costo_intervento,
main_verifica.note_verifica
"""

#
DB_COLUM_SEARCH_ID ="""
main_cliente.numero_cellulare,
main_cliente.via,
main_cliente.nome,
main_cliente.cognome,
main_cliente.codice_fiscale,
main_cliente.cliente_data_inserimento,
main_cliente.numero_telefono,
main_cliente.mail,
main_cliente.citta,
main_cliente.id AS cliente_id,
main_impianto.modello_caldaia,
main_impianto.impianto_data_inserimento,
main_impianto.matricola_caldaia,
main_impianto.combustibile,
main_impianto.data_installazione,
main_impianto.data_contratto,
main_impianto.tipo_caldaia,
main_impianto.altro_tipo_caldaia,
main_impianto.potenza_caldaia,
main_impianto.altra_potenza_caldaia,
main_impianto.marca_caldaia,
main_impianto.codice_impianto,
main_impianto.id AS impianto_id,
main_intervento.note_intervento,
main_intervento.tipo_intervento,
main_intervento.data_intervento,
main_intervento.id AS intervento_id,
main_verifica.stato_verifica,
main_verifica.data_verifica,
main_verifica.tipo_verifica,
main_verifica.altro_tipo_verifica,
main_verifica.codice_id,
main_verifica.numero_rapporto,
main_verifica.prossima_verifica,
main_verifica.colore_bollino,
main_verifica.numero_bollino,
main_verifica.valore_bollino,
main_verifica.analisi_combustione,
main_verifica.prossima_analisi_combustione,
main_verifica.stato_pagamento,
main_verifica.costo_intervento,
main_verifica.note_verifica,
main_verifica.id AS verifica_id
"""
DB_FROM_JOIN = """
main_cliente
LEFT JOIN main_impianto ON main_impianto.cliente_impianto_id = main_cliente.id
LEFT JOIN main_verifica ON main_verifica.verifica_impianto_id = main_impianto.id
LEFT JOIN main_intervento ON main_intervento.intervento_impianto_id = main_impianto.id
"""
DB_FROM_JOIN_IMPIANTO = """
main_cliente
LEFT JOIN main_impianto ON main_impianto.cliente_impianto_id = main_cliente.id
"""
DB_ORDER = " ORDER BY main_cliente.cognome ASC, main_cliente.nome ASC"

QUERY = """
SELECT
    main_cliente.numero_cellulare,
    main_cliente.via,
    main_cliente.nome,
    main_cliente.cognome,
    main_cliente.codice_fiscale,
    main_cliente.cliente_data_inserimento,
    main_cliente.numero_telefono,
    main_cliente.mail,
    main_cliente.citta,
    main_cliente.id AS cliente_id,
    main_impianto.modello_caldaia,
    main_impianto.impianto_data_inserimento,
    main_impianto.matricola_caldaia,
    main_impianto.combustibile,
    main_impianto.data_installazione,
    main_impianto.data_contratto,
    main_impianto.tipo_caldaia,
    main_impianto.altro_tipo_caldaia,
    main_impianto.potenza_caldaia,
    main_impianto.altra_potenza_caldaia,
    main_impianto.marca_caldaia,
    main_impianto.codice_impianto,
    main_impianto.id AS impianto_id,
    main_intervento.note_intervento,
    main_intervento.tipo_intervento,
    main_intervento.data_intervento,
    main_intervento.id AS intervento_id
FROM
    main_cliente
    LEFT JOIN main_impianto ON main_impianto.cliente_impianto_id = main_cliente.id
    LEFT JOIN main_intervento ON main_intervento.intervento_impianto_id = main_impianto.id
"""
QUERY_ORDER = "ORDER BY main_cliente.cognome ASC, main_cliente.nome ASC"

QUERY_WHERE = """
(
    UPPER(main_cliente.nome::text) LIKE UPPER(%s) OR
    UPPER(main_cliente.numero_cellulare::text) LIKE UPPER(%s) OR
    UPPER(main_cliente.via::text) LIKE UPPER(%s) OR
    UPPER(main_cliente.nome::text) LIKE UPPER(%s) OR
    UPPER(main_cliente.cognome::text) LIKE UPPER(%s) OR
    UPPER(main_cliente.codice_fiscale::text) LIKE UPPER(%s) OR
    UPPER(main_cliente.numero_telefono::text) LIKE UPPER(%s) OR
    UPPER(main_cliente.mail::text) LIKE UPPER(%s) OR
    UPPER(main_cliente.citta::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.modello_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.matricola_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.combustibile::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.tipo_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.potenza_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.altro_tipo_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.altra_potenza_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.marca_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.codice_impianto::text) LIKE UPPER(%s) OR
    UPPER(main_intervento.note_intervento::text) LIKE UPPER(%s) OR
    UPPER(main_intervento.tipo_intervento::text) LIKE UPPER(%s)
)
"""

QUERY2 = """
SELECT
    main_verifica.data_verifica,
    main_verifica.stato_verifica,
    main_verifica.tipo_verifica,
    main_verifica.altro_tipo_verifica,
    main_verifica.codice_id,
    main_verifica.numero_rapporto,
    main_verifica.prossima_verifica,
    main_verifica.colore_bollino,
    main_verifica.numero_bollino,
    main_verifica.valore_bollino,
    main_verifica.analisi_combustione,
    main_verifica.prossima_analisi_combustione,
    main_verifica.stato_pagamento,
    main_verifica.costo_intervento,
    main_verifica.note_verifica,
    main_verifica.id AS verifica_id,
    main_verifica.verifica_impianto_id
FROM main_verifica
WHERE
"""

QUERY2_WHERE ="""
    (
        main_verifica.verifica_impianto_id = ANY (%s)
    )
"""
QUERY2_ORDER ="ORDER BY main_verifica.data_verifica DESC"

def search_runQuery(query_str, param):
    #print ">> " + query_str + " <<"
    cursor = connection.cursor()
    cursor.execute(query_str, param)
    desc = cursor.description

    l = []
    for col in desc:
        c = col[0]
        l.append(c)

    return [ dict(zip(l, row))
            for row in cursor.fetchall() ]

def search_clienteId(id):
    query_str = "SELECT " + DB_COLUM_SEARCH_ID + " FROM " + DB_FROM_JOIN
    query_str += " WHERE main_cliente.id = %s " + DB_ORDER
    return search_runQuery(query_str, [id])

def search_impiantoId(id):
    query_str = "SELECT " + DB_COLUM_SEARCH_ID + " FROM " + DB_FROM_JOIN
    query_str += " WHERE main_impianto.id = %s " + DB_ORDER
    return search_runQuery(query_str, [id])

def search_verificaId(id):
    query_str = "SELECT " + DB_COLUM_SEARCH_ID + " FROM " + DB_FROM_JOIN
    query_str +=" WHERE main_verifica.id = %s " + DB_ORDER
    return search_runQuery(query_str, [id])

def search_interventoId(id):
    query_str = "SELECT " + DB_COLUM_SEARCH_ID + " FROM " + DB_FROM_JOIN
    query_str += " WHERE main_intervento.id = %s " + DB_ORDER
    return search_runQuery(query_str, [id])

def query_test(test_str):
    return []

def query_table(query_str, param, query_str2=None, param2=None):
    """
    We split the query in two, one select clienti and impiato, and
    with the ids, we selct the verifiche table.
    """
    l1 = search_runQuery(query_str, param)

    # Get the ids of all impiati select
    param = []
    for i in l1:
        if i['impianto_id'] is None:
            continue

        param.append(i['impianto_id'])

    if not param:
        return l1

    # if we want to specify a different second query we pass explict sql string
    if query_str2 is None:
        query_str = QUERY2 + " ( " + QUERY2_WHERE + " ) " +  QUERY2_ORDER
    else:
        query_str = QUERY2 + " ( " + QUERY2_WHERE + " AND " + query_str2 + " ) " +  QUERY2_ORDER
        param = param + param2

    cursor = connection.cursor()
    cursor.execute(query_str, param)
    desc = cursor.description
    l = [col[0] for col in desc]

    # Get all verifiche data structed as: dict of list
    # { impianto_id : [ verifiche list] }
    l2 = {}
    for row in cursor.fetchall():
        d = dict(zip(l, row))
        key = d['verifica_impianto_id']
        if l2.has_key(key):
            l2[key].append(d)
        else:
            l2[key] = [d]

    # Compute the last verifica and the most recent
    # analisi combustione, with its id.
    n = []
    for j in l1:
        if j['impianto_id'] is not None and l2.has_key(j['impianto_id']):
            verifiche_list = l2[j['impianto_id']]
            if verifiche_list:
                row = verifiche_list[0]
                row['data_ultima_verifica'] = row['data_verifica']
                for i in verifiche_list:
                    if i['analisi_combustione']:
                        row['ultima_analisi_combustione'] = i['data_verifica']
                        row['ultima_analisi_combustione_id'] = i['verifica_id']
                        row['prossima_analisi_combustione'] = i['prossima_analisi_combustione']
                        break
                n.append(dict(j.items() + row.items()))
    return n

def generate_query(s):
    search_key = []
    if " " in s:
        search_key = s.strip().split(" ")
    else:
        search_key.append(s.strip())

    param = []
    search_query_str = ""
    for i, key in enumerate(search_key):
        # If the search string is less than 3 char, we search key on
        # start string, otherwise we search as contain
        if len(key) >= 3:
            key = "%" + key + "%"
        else:
            key = key + "%"

        # count number of param to build the list
        param += [key] * QUERY_WHERE.count("%s")
        search_query_str += QUERY_WHERE

        if (i == 0 and len(search_key) > 1) or i < len(search_key) - 1:
            search_query_str += " AND "

    return QUERY + " WHERE ( " + search_query_str + " ) " + QUERY_ORDER, param

def search_inMonth(key=None, month=None, year=None, filter=None):
    if month is None:
        month = datetime.date.today().month
    if year is None:
        year = datetime.date.today().year

    if month > 12 and month < 1:
        logger.error("Invalid month[%s]" % month)
        return []

    query_str = QUERY + QUERY_ORDER
    param = []
    if key is not None:
        query_str, param = generate_query(key)


    query_year = """(
        main_verifica.prossima_analisi_combustione BETWEEN \'%s-01-01 00:00:00\' and \'%s-12-31 23:59:59.999999\' OR
        main_verifica.prossima_verifica BETWEEN \'%s-01-01 00:00:00\' and \'%s-12-31 23:59:59.999999\'
        )""" % (year, year, year, year)

    query_month = """(
        EXTRACT(\'month\' FROM main_verifica.prossima_analisi_combustione) = %s OR
        EXTRACT(\'month\' FROM main_verifica.prossima_verifica) = %s
        )""" % (month, month)

    if filter == 'fumi':
        query_year = "( main_verifica.prossima_analisi_combustione BETWEEN \'%s-01-01 00:00:00\' and \'%s-12-31 23:59:59.999999\')" % (year, year)
        query_month = "( EXTRACT(\'month\' FROM main_verifica.prossima_analisi_combustione) = %s )" % month
    if filter == 'verifiche':
        query_year = "( main_verifica.prossima_verifica BETWEEN \'%s-01-01 00:00:00\' and \'%s-12-31 23:59:59.999999\')" % (year, year)
        query_month = "( EXTRACT(\'month\' FROM main_verifica.prossima_verifica) = %s )" % month

    query_str2 = " ( " + query_year + " AND " + query_month + " )"
    return query_table(query_str, param, query_str2, [])


def search_fullText(s):
    query_str, param = generate_query(s)
    return query_table(query_str, param)


