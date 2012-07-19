#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import decimal
import string

from tools import *
from django.db.models import Q
from django.forms.models import model_to_dict

from models import Cliente


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
#    dump(r)
    node.save()
    return node

def record_toDict(record):
    record_dict = model_to_dict(record)
    if type(record) == models.Cliente:
        record_dict['cliente_id'] = record_dict['id']
    if type(record) == models.Impianto:
        record_dict['impianto_id'] = record_dict['id']

    del record_dict['id']
    return record_dict

def table_doDict(clienti_selection):
    table = []
    clienti_items = clienti_selection.select_related().values()
    for i in clienti_items:
        row = {}
        impianto_items = models.Cliente.objects.get(pk=i['id']).impianto_set.values()
        for j in impianto_items:
            row = dict(i.items() + j.items())
            row['cliente_id'] = i['id']
            row['impianto_id'] = j['id']

            verifichemanutenzione_items = models.Impianto.objects.get(pk=j['id']).verifichemanutenzione_set.values()
            if verifichemanutenzione_items:
                row = dict(row.items() + verifichemanutenzione_items[0].items())
                row['verifiche_id'] = verifichemanutenzione_items[0]['id']
                del row['id']
                table.append(row)

            intervento_items = models.Impianto.objects.get(pk=j['id']).intervento_set.values()
            if intervento_items:
                row = dict(row.items() + intervento_items[0].items())
                row['intervento_id'] = intervento_items[0]['id']
                del row['id']
                table.append(row)

            if verifichemanutenzione_items == [] and intervento_items == []:
                del row['id']
                table.append(row)

    return table

def my_custom_sql(param):
    from django.db import connection, transaction
    cursor = connection.cursor()

    cursor.execute("select c.*, i.* from main_cliente as c join main_impianto as i on i.cliente_impianto_id = c.id where c.cognome like %s order by c.nome desc", param)
    row = cursor.fetchall()

    return row

def search_fullText(ctx, s):
    """
    If users search one word and is number we search only in some
    table field, otherwise apply some euristic to make a full text search
    on all db fields
    """
    result = []

    if ":" in s:
        if "pk:" in s:
            _, pk = s.strip().split(":")
            return [select_record(ctx, pk)]

        key, value = s.strip().split(":")
        return  ctx.filter(**{ key + '__icontains' : value })

    search_key = []
    if " " in s:
        search_key = s.strip().split(" ")
    else:
        search_key.append(s.strip())

    for key in search_key:
        if len(key) >= 3:
            result = ctx.filter(Q(numero_telefono__icontains = key) |
                           Q(numero_cellulare__icontains = key) |
                           Q(nome__icontains = key) |
                           Q(cognome__icontains = key) |
                           Q(via__icontains = key) |
                           Q(citta__icontains = key) |
                           Q(mail__icontains = key)
                           )
        else:
            if key[0] in string.letters:
                result = ctx.filter(Q(nome__istartswith = key) |
                               Q(cognome__istartswith = key) |
                               Q(citta__istartswith = key))
        ctx = result
        # Print the current query_set
        #print result.query

    return result
