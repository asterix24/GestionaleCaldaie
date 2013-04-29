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
from main import cfg

import logging
logger = logging.getLogger(__name__)


QUERY = """
SELECT
    *,
    main_cliente.id AS cliente_id,
    age(main_impianto.data_installazione) AS anzianita_impianto,
    main_impianto.id AS impianto_id
FROM
    main_cliente
    LEFT JOIN main_impianto ON main_impianto.cliente_impianto_id = main_cliente.id
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
    UPPER(main_cliente.cap::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.modello_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.matricola_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.combustibile::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.tipo_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.potenza_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.altro_tipo_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.altra_potenza_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.marca_caldaia::text) LIKE UPPER(%s) OR
    UPPER(main_impianto.codice_impianto::text) LIKE UPPER(%s)
)
"""

QUERY_VERIFICHE = """
SELECT
    *,
    main_verifica.id AS verifica_id
FROM main_verifica
WHERE
"""

QUERY_WHERE_VERIFICHE ="""
    (
        main_verifica.verifica_impianto_id IN (%s)
    )
"""

QUERY_ORDER_VERIFICHE ="ORDER BY main_verifica.data_verifica DESC"

QUERY_INTERVENTO = """
SELECT
    *,
    main_intervento.id AS intervento_id
FROM main_intervento
WHERE
(
    main_intervento.data_intervento = (SELECT MAX(main_intervento.data_intervento) from main_intervento where intervento_impianto_id IN (%s))
)
ORDER BY main_intervento.data_intervento DESC
"""

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

#
DB_COLUM_SEARCH_ID ="""
SELECT
    *,
    main_cliente.id AS cliente_id,
    age(main_impianto.data_installazione) AS anzianita_impianto,
    main_impianto.id AS impianto_id,
    main_intervento.id AS intervento_id,
    main_verifica.id AS verifica_id
FROM
    main_cliente
    LEFT JOIN main_impianto ON main_impianto.cliente_impianto_id = main_cliente.id
    LEFT JOIN main_verifica ON main_verifica.verifica_impianto_id = main_impianto.id
    LEFT JOIN main_intervento ON main_intervento.intervento_impianto_id = main_impianto.id
WHERE
"""

def search_clienteId(id):
    query_str = DB_COLUM_SEARCH_ID
    query_str += "main_cliente.id = %s "
    query_str += "ORDER BY main_cliente.cognome ASC, main_cliente.nome ASC"
    return search_runQuery(query_str, [id])

def search_impiantoId(id):
    query_str = DB_COLUM_SEARCH_ID
    query_str += "main_impianto.id = %s "
    query_str += "ORDER BY main_impianto.data_installazione DESC"
    return search_runQuery(query_str, [id])

def search_verificaId(id):
    query_str = DB_COLUM_SEARCH_ID
    query_str +=" WHERE main_verifica.id = %s "
    query_str += "ORDER BY main_verifica.data_verifica DESC"
    return search_runQuery(query_str, [id])

def search_interventoId(id):
    query_str = DB_COLUM_SEARCH_ID
    query_str +=" WHERE main_intervento.id = %s "
    query_str +="ORDER BY main_intervento.data_intervento DESC"
    return search_runQuery(query_str, [id])


def query_test(id):
    cli = Cliente.object.get(pk=id)


    return []

def __impiantiIds(field, query_data):
    l = []
    for i in query_data:
        id = i.get(field, None)
        if id is None:
            continue

        l.append(str(id))
    return ",".join(l)

def query_table(query_str, param, query_str2=None, param2=None, verifiche_only=False):
    """
    We split the query in two, one select clienti and impiato, and
    with the ids, we selct the verifiche table.
    """
    query_data = search_runQuery(query_str, param)

    # Get the ids of all impiati select
    s = __impiantiIds('impianto_id', query_data)
    if s == "":
        return query_data

    query_where_verifiche = QUERY_WHERE_VERIFICHE % (s)
    query_interventi = QUERY_INTERVENTO % (s)

    # if we want to specify a different second query we pass explict sql string
    if query_str2 is None:
        query_str = QUERY_VERIFICHE + " ( " + query_where_verifiche + " ) " +  QUERY_ORDER_VERIFICHE
    else:
        query_str = QUERY_VERIFICHE + " ( " + query_where_verifiche + " AND " + query_str2 + " ) " +  QUERY_ORDER_VERIFICHE
        param = param + param2

    #print query_str
    cursor = connection.cursor()
    cursor.execute(query_str, param)
    desc = cursor.description
    l = [col[0] for col in desc]

    # Get all verifiche data structed as: dict of list
    # { impianto_id : [ verifiche list] }
    query_data2 = {}
    for row in cursor.fetchall():
        d = dict(zip(l, row))
        key = d['verifica_impianto_id']
        if query_data2.has_key(key):
            query_data2[key].append(d)
        else:
            query_data2[key] = [d]

    #print query_str
    cursor = connection.cursor()
    cursor.execute(query_interventi, param)
    desc = cursor.description
    l = [col[0] for col in desc]

    # Get all interventi data structed as: dict of list
    # { impianto_id : [ interventi list] }
    query_data3 = {}
    for row in cursor.fetchall():
        d = dict(zip(l, row))
        key = d['intervento_impianto_id']
        if query_data3.has_key(key):
            query_data3[key].append(d)
        else:
            query_data3[key] = [d]

    # Compute the last verifica and the most recent
    # analisi combustione, with its id.
    n = []
    for table_row in query_data:
        interventi_row = {}
        verifiche_row = {}

        id = table_row.get('impianto_id', None)
        if id is not None:
            #verifiche
            verifiche_list = query_data2.get(id, [])
            if verifiche_list:
                verifiche_row = verifiche_list[0]
                verifiche_row['data_ultima_verifica'] = verifiche_row['data_verifica']
                for i in verifiche_list:
                    if i['analisi_combustione']:
                        verifiche_row['ultima_analisi_combustione'] = i['data_verifica']
                        verifiche_row['ultima_analisi_combustione_id'] = i['verifica_id']
                        verifiche_row['prossima_analisi_combustione'] = i['prossima_analisi_combustione']
                        break

            interventi_list = query_data3.get(id, [])
            if interventi_list:
                interventi_row = interventi_list[0]

            if verifiche_only and verifiche_list:
                n.append(dict(table_row.items() + verifiche_row.items()))
            elif not verifiche_only and (verifiche_list or interventi_list):
                n.append(dict(table_row.items() + verifiche_row.items() + interventi_row.items()))

        elif not verifiche_only:
            n.append(table_raw)

    return n

def generate_query(search_keys=None, order_by_field=None, ordering=None, id_field='',ids=[]):
    query_order = QUERY_ORDER

    if order_by_field is not None and order_by_field != "":
        if ordering is None:
            ordering = "ASC"
        print order_by_field
        if 'main_cliente' in order_by_field or 'main_impianto' in order_by_field:
            query_order = "ORDER BY " + order_by_field + " " + ordering + ", main_cliente.cognome ASC, main_cliente.nome ASC"


    if search_keys is None and ids == []:
        return QUERY + query_order, []

    param = []
    search_query = []
    query_str = ""

    if search_keys is not None:
        search_key = []
        if " " in search_keys:
            search_key = search_keys.strip().split(" ")
        else:
            search_key.append(search_keys.strip())

        for i, key in enumerate(search_key):
            # If the search string is less than 3 char, we search key on
            # start string, otherwise we search as contain
            if len(key) >= 3:
                key = "%" + key + "%"
            else:
                key = key + "%"

            # count number of param to build the list
            param += [key] * QUERY_WHERE.count("%s")
            search_query.append(QUERY_WHERE)

    if ids and id_field != '':
        search_query.append("(%s IN (%s))" % (id_field, ",".join(ids)))


    return QUERY + " WHERE ( " + " AND ".join(search_query)  + " ) " + query_order, param

def search_inMonth(search_keys=None, ref_month=None, ref_year=None, filter_type=None, order_by_field=None, ordering=None):

    if ref_month is None or ref_month == "":
        ref_month = datetime.date.today().month
    if ref_year is None or ref_year == "":
        ref_year = datetime.date.today().year

    if ref_month > 12 and ref_month < 1:
        logger.error("Invalid month[%s]" % ref_month)
        return []

    #if group_field is not None:
    query_str, param = generate_query(search_keys, order_by_field, ordering)


    query_year = """(
        ( EXTRACT(\'year\' FROM main_verifica.data_verifica) < %s AND main_verifica.analisi_combustione) OR
        ( EXTRACT(\'year\' FROM main_verifica.prossima_analisi_combustione) < %s) OR
        ( EXTRACT(\'year\' FROM main_verifica.data_verifica) < %s) OR
        ( EXTRACT(\'year\' FROM main_verifica.prossima_verifica) < %s)
        )""" % (ref_year, ref_year, ref_year, ref_year)

    query_month = """(
        ( EXTRACT(\'month\' FROM main_verifica.data_verifica) = %s AND main_verifica.analisi_combustione) OR
        ( EXTRACT(\'month\' FROM main_verifica.prossima_analisi_combustione) = %s ) OR
        ( EXTRACT(\'month\' FROM main_verifica.data_verifica) = %s ) OR
        ( EXTRACT(\'month\' FROM main_verifica.prossima_verifica) = %s )
        )""" % (ref_month, ref_month, ref_month, ref_month)

    if filter == 'fumi':
        query_year = "( EXTRACT(\'year\' FROM main_verifica.data_verifica) < %s AND main_verifica.analisi_combustione)" % (ref_year)
        query_month = "( EXTRACT(\'month\' FROM main_verifica.data_verifica) = %s AND main_verifica.analisi_combustione)" % (ref_month)

    if filter == 'fumi_prossimi':
        query_year = "( EXTRACT(\'year\' FROM main_verifica.prossima_analisi_combustione) < %s)" % (ref_year)
        query_month = "( EXTRACT(\'month\' FROM main_verifica.prossima_analisi_combustione) = %s )" % (ref_month)

    if filter == 'verifiche':
        query_year = "( EXTRACT(\'year\' FROM main_verifica.data_verifica) < %s)" % (ref_year)
        query_month = "( EXTRACT(\'month\' FROM main_verifica.data_verifica) = %s )" % (ref_month)

    if filter == 'verifiche_prossima':
        query_year = "( EXTRACT(\'year\' FROM main_verifica.prossima_verifica) < %s)" % (ref_year)
        query_month = "( EXTRACT(\'month\' FROM main_verifica.prossima_verifica) = %s )" % (ref_month)

    query_str2 = " ((main_verifica.stato_verifica = \'A\' OR main_verifica.stato_verifica = \'S\') AND " + query_year + " AND " + query_month + " )"

    data = query_table(query_str, param, query_str2, [], verifiche_only=True)
    return query_sortDict(data, order_by_field, ordering)



def query_sortDict(data, order_by_field, ordering):

    try:
        _, order_by_field = order_by_field.split('.')
    except (ValueError, KeyError), m:
        logger.error("%s Errore nello split di %s" % (__name__, order_by_field))

    if ordering == 'asc':
        ordering = False
    else:
        ordering = True

    def __sortDict(d):
        d = d.get(order_by_field, None)
        if order_by_field in cfg.DB_DATA_FIELD:
            if d is None:
                return datetime.date(2000,1,1)
        return d

    return sorted(data, key=__sortDict, reverse=ordering)

def search_fullText(search_keys=None, order_by_field=None, ordering=None):
    query_str, param = generate_query(search_keys, order_by_field, ordering)
    data = query_table(query_str, param)
    return query_sortDict(data, order_by_field, ordering)

def search_ids(id_field, ids):
    query_str, param = generate_query(id_field=id_field,ids=ids)
    return query_table(query_str, param)


