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


FILTER_MODE_START =    '__istartswith'
FILTER_MODE_EXACT =    '__iexact'
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

#FROM
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

#WHERE

DB_WHERE_LIKE = """
(
main_cliente.numero_cellulare ILIKE %s OR
main_cliente.via ILIKE %s OR
main_cliente.nome ILIKE %s OR
main_cliente.cognome ILIKE %s OR
main_cliente.codice_fiscale ILIKE %s OR
main_cliente.numero_telefono ILIKE %s OR
main_cliente.mail ILIKE %s OR
main_cliente.citta ILIKE %s OR
main_impianto.modello_caldaia ILIKE %s OR
main_impianto.matricola_caldaia ILIKE %s OR
main_impianto.combustibile ILIKE %s OR
main_impianto.tipo_caldaia ILIKE %s OR
main_impianto.potenza_caldaia ILIKE %s OR
main_impianto.altro_tipo_caldaia ILIKE %s OR
main_impianto.altra_potenza_caldaia ILIKE %s OR
main_impianto.marca_caldaia ILIKE %s OR
main_impianto.codice_impianto ILIKE %s OR
main_intervento.note_intervento ILIKE %s OR
main_intervento.tipo_intervento ILIKE %s OR
main_verifica.colore_bollino ILIKE %s OR
CAST(main_verifica.numero_bollino AS TEXT) ILIKE %s OR
main_verifica.tipo_verifica ILIKE %s OR
main_verifica.altro_tipo_verifica ILIKE %s OR
main_verifica.note_verifica ILIKE %s OR
main_verifica.numero_rapporto ILIKE %s
)
"""

"""
 DISTINCT

"""

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
    main_intervento.id AS intervento_id,
    tabella_verifica.stato_verifica,
    tabella_verifica.tipo_verifica,
    tabella_verifica.altro_tipo_verifica,
    tabella_verifica.codice_id,
    tabella_verifica.numero_rapporto,
    tabella_verifica.prossima_verifica,
    tabella_verifica.colore_bollino,
    tabella_verifica.numero_bollino,
    tabella_verifica.valore_bollino,
    tabella_verifica.analisi_combustione,
    tabella_verifica.prossima_analisi_combustione,
    tabella_verifica.stato_pagamento,
    tabella_verifica.costo_intervento,
    tabella_verifica.note_verifica,
    tabella_verifica.id AS verifica_id,
    tabella_verifica.data_verifica AS data_ultima_verifica,
    ultima_analisi_fumi.data_verifica AS ultima_analisi_combustione,
    ultima_analisi_fumi.id AS ultima_analisi_combustione_id
FROM
    main_cliente
    LEFT JOIN main_impianto ON main_impianto.cliente_impianto_id = main_cliente.id
    LEFT JOIN main_intervento ON main_intervento.intervento_impianto_id = main_impianto.id,
    (
        SELECT
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
        main_verifica.id
        FROM main_verifica
        WHERE main_verifica.verifica_impianto_id = main_impianto.id
        ORDER BY main_verifica.data_verifica DESC
        LIMIT 1
    ) tabella_verifica,
    (
        SELECT main_verifica.analisi_combustione, main_verifica.data_verifica, main_verifica.id
        FROM main_verifica
        WHERE main_verifica.analisi_combustione = true AND main_verifica.verifica_impianto_id = main_impianto.id
        ORDER BY main_verifica.data_verifica DESC
        LIMIT 1
    ) ultima_analisi_fumi
WHERE
(
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
        UPPER(main_intervento.tipo_intervento::text) LIKE UPPER(%s) OR
        UPPER(tabella_verifica.colore_bollino::text) LIKE UPPER(%s) OR
        UPPER(CAST(tabella_verifica.numero_bollino AS TEXT)) LIKE UPPER(%s) OR
        UPPER(tabella_verifica.tipo_verifica::text) LIKE UPPER(%s) OR
        UPPER(tabella_verifica.altro_tipo_verifica::text) LIKE UPPER(%s) OR
        UPPER(tabella_verifica.note_verifica::text) LIKE UPPER(%s) OR
        UPPER(tabella_verifica.numero_rapporto::text) LIKE UPPER(%s)
    )
)
ORDER BY main_cliente.cognome ASC, main_cliente.nome ASC
"""


# AND
DB_WHERE_SUBQUERY = """
(
    main_verifica.data_verifica =
    (
        SELECT MAX(main_verifica.data_verifica)
        FROM main_verifica
        WHERE verifica_impianto_id = main_impianto.id
    )
    OR
        main_verifica.verifica_impianto_id IS NULL
)
"""

DB_WHERE_SUBQUERY_NULL = """
        main_verifica.verifica_impianto_id IS NULL
"""

DB_WHERE_SUBQUERY_FUMI = """
(
    main_verifica.data_verifica =
    max((
        SELECT CASE WHEN main_verifica.analisi_combustione THEN main_verifica.data_verifica END AS data_ultima_analisi
            FROM  main_verifica GROUP BY main_verifica.data_verifica, main_verifica.analisi_combustione
    ))
)
"""

DB_ORDER = " ORDER BY main_cliente.cognome ASC, main_cliente.nome ASC"

def filter_query(data):
    max_date = None
    for i in data:
        d = i['data_verifica']
        print d
        if d is not None:
            if max_date is None:
                max_date = d
            if d > max_date:
                max_date = d

    print "il max e': %s" % max_date



def search_runQuery(query_str, param):
    #print ">> " + query_str + " <<"
    cursor = connection.cursor()
    cursor.execute(query_str, param)

    desc = cursor.description
    l = []
    i = 0
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
    query_str = QUERY
    test_str = [test_str] * query_str.count("%s")
    return search_runQuery(query_str, test_str)

def search_dataRange(key, start, end):
    query_str = "SELECT " + DB_COLUM + " FROM " + DB_FROM_JOIN
    query_str += " WHERE (main_verifica.prossima_analisi_combustione BETWEEN \'2010-01-01 00:00:00\' and \'2010-12-31 23:59:59.999999\' AND EXTRACT(\'month\' FROM main_verifica.prossima_analisi_combustione) = 9) "
    query_str += DB_ORDER

    return search_runQuery(query_str, [key])

def search_fullText(s):
    search_key = []
    if " " in s:
        search_key = s.strip().split(" ")
    else:
        search_key.append(s.strip())

    #query_str = "SELECT " + DB_COLUM + " FROM " + DB_FROM_JOIN + " WHERE "

    param = []
    for i, key in enumerate(search_key):
        if len(key) >= 3:
            key = "%" + key + "%"
        else:
            key = key + "%"

        #query_str += DB_WHERE_LIKE
        param += [key] * QUERY.count("%s")

        if (i == 0 and len(search_key) > 1) or i < len(search_key) - 1:
            query_str += " AND "

    #query_str += " AND " + DB_WHERE_SUBQUERY  + " AND " + DB_WHERE_SUBQUERY_FUMI
    #query_str += " AND " + DB_WHERE_SUBQUERY_FUMI
    #query_str += DB_ORDER

    return search_runQuery(QUERY, param)

