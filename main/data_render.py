#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import models

logger = logging.getLogger(__name__)

DATA_FIELD_STR_FORMAT = "%d/%m/%Y"
MSG_ITEMS_EMPTY = "<br><tr><h2>La ricerca non ha prodotto risultati</h2></tr><br>"
EMPTY_CELL = '<center>-</center>'
ACTION_DICT = {
        'add':'plus.jpg',
        'delete':'minus.jpg',
        'edit':'edit.jpg'
        }

def make_url(type, action, message, path, cliente_id=None, impianto_id=None, sub_impianto_id=None):
    data = ""
    url = "<a href=\""
    if path.count('%s') == 3:
        url += path % (cliente_id, impianto_id, sub_impianto_id)
    elif path.count('%s') == 2:
        url += path % (cliente_id, impianto_id)
    elif path.count('%s') == 1:
        url += path % (cliente_id)
    else:
        return "errore!"

    if type == 'icon':
        url += "\">"
        data += "<img src=\"/static/%s\" alt=\"%s..\" title=\"%s..\" width=\"16\" height=\"16\"/> " % (ACTION_DICT[action], action, action)
    elif type == 'button':
        url += "\" name=\"href_button\">"
    else:
        url += "\">"

    data += "%s"  % message
    return url + data + "</a>"


def isValidKey(items, key):
    if items[key] is None or items[key] == "":
        return False
    return True

def __cliente_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    return make_url('','', items[key], '/anagrafe/%s/', items['cliente_id'])

def __impianto_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    return make_url('','', items[key], '/anagrafe/%s/impianto/%s/',
            items['cliente_id'], items['impianto_id'])

def __verifica_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return "Nessuna verifica"

    str = items[key]
    if type(str) == datetime.date:
        str = str.strftime(DATA_FIELD_STR_FORMAT)
    return make_url('','', str, '/anagrafe/%s/impianto/%s/verifica/%s/',
            items['cliente_id'], items['impianto_id'], items['verifica_id'])

def __ultima_analisi_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return "No Fumi"

    str = items[key]
    if type(str) == datetime.date:
        str = str.strftime(DATA_FIELD_STR_FORMAT)
    return make_url('','', str, '/anagrafe/%s/impianto/%s/verifica/%s/',
            items['cliente_id'], items['impianto_id'], items['ultima_analisi_combustione_id'])

def __tipo_caldaia(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    str = items[key]
    if str.lower() == 'altro':
        s = items['altro_tipo_caldaia']
    else:
        s = items[key]

    return s

def __tipo_verifica(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return "No Manutezioni"

    str = items[key]
    if str.lower() == 'altro':
        s = items['altro_tipo_verifica']
    else:
        if str in models.VERIFICHE_TYPE_CHOISES_DICT:
            s = models.VERIFICHE_TYPE_CHOISES_DICT[str]

    return s

def __colore_bollino(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    str = items[key]
    if str.lower() == 'altro':
        s = items['altro_colore_bollino']
    else:
        if str in models.BOLLINO_COLOR_CHOICES_DICT:
            s = models.BOLLINO_COLOR_CHOICES_DICT[str]

    return s

def __analisi_combustione(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return "No Fumi"

    s = 'No.'
    if items[key]:
        s = 'Eseguita.'

    return s


def __stato_pagamento(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    s = "Da riscuotere."
    if items[key]:
        s = "Pagato!"

    return s


RENDER_TABLE_URL = {
    'nome': __cliente_url,
    'cognome': __cliente_url,
    'codice_impianto': __impianto_url,
    'matricola_caldaia': __impianto_url,
    'modello_caldaia': __impianto_url,
    'marca_caldaia': __impianto_url,
    'data_verifica': __verifica_url,
    'data_ultima_verifica': __verifica_url,
    'ultima_analisi_combustione': __ultima_analisi_url,
}

RENDER_TABLE = {
    'tipo_caldaia': __tipo_caldaia,
    'tipo_verifica': __tipo_verifica,
    'colore_bollino': __colore_bollino,
    'analisi_combustione': __analisi_combustione,
    'stato_pagamento': __stato_pagamento,
}

def formatFields(item_dict, field_name, with_url=False, default_text=EMPTY_CELL):
    try:
        s = default_text
        if item_dict.has_key(field_name):
            if field_name in RENDER_TABLE:
                s = RENDER_TABLE[field_name](item_dict, field_name, default_text)
            elif with_url and field_name in RENDER_TABLE_URL:
                s = RENDER_TABLE_URL[field_name](item_dict, field_name, default_text)
            else:
                s  = item_dict[field_name]
                if not isValidKey(item_dict, field_name):
                    s = default_text
                elif type(s) == datetime.date:
                    s = s.strftime(DATA_FIELD_STR_FORMAT)

    except (KeyError, ValueError), m:
        logger.error("%s Errore nel render di %s (%s) s=%s {%s}" % (__name__, i, m, s, item_dict))
        s = default_text

    return s

class DataRender(object):
    def __init__(self, items, msg_items_empty = MSG_ITEMS_EMPTY):
        self.items = items
        self.colums = None
        self.display_header = True
        self.msg_items_empty = msg_items_empty
        self.url_type = []
        self.detail_type = None
        self.url_add = None
        self.unique_row = False

    def showHeader(self, display_header):
        self.display_header = display_header

    def uniqueRow(self, unique_row):
        self.unique_row = unique_row

    def msgItemsEmpty(self, msg):
        self.msg_items_empty = msg

    def selectColums(self, colums):
        self.colums = colums

    def urlBar(self, detail_type, url_type):
        self.detail_type = detail_type
        self.url_type = url_type

    def toTable(self):
        if self.items == []:
            return self.msg_items_empty

        duplicate_row = {}
        cycle = False
        table = "<table id=\"customers\">"
        for item_dict in self.items:
            if self.display_header:
                table += "<tr>"
                table += "<th></th>"
                for j in self.colums:
                    table += "<th>%s</th>" % j.replace('_', ' ').capitalize()
                table += "</tr>"
                self.display_header = False

            skip_row = False
            if self.unique_row:
                key = ""
                for i in self.colums:
                    key += "%s" % item_dict[i]
                if duplicate_row.has_key(key):
                    skip_row = True
                else:
                    duplicate_row[key] = ""

            if not skip_row:
                skip_row = False

                cycle_str = ''
                if cycle:
                    cycle_str = " class=\"alt\""
                cycle = not cycle

                table += "<tr%s>" % cycle_str
                if self.detail_type is not None:
                    p = ''
                    for j in self.url_type:
                        if self.detail_type == 'cliente':
                            p += make_url('icon', j, '', '/anagrafe/%s/' + j + "/", cliente_id=item_dict['cliente_id'])
                        elif self.detail_type == 'impianto':
                            p += make_url('icon', j, '', '/anagrafe/%s/impianto/%s/' + j + "/",
                                    cliente_id=item_dict['cliente_id'], impianto_id=item_dict['impianto_id'])
                        else:
                            p += make_url('icon', j, '', '/anagrafe/%s/impianto/%s/' + self.detail_type + "/%s/" + j + "/",
                                    cliente_id=item_dict['cliente_id'],
                                    impianto_id=item_dict['impianto_id'],
                                    sub_impianto_id=item_dict[self.detail_type + '_id'])

                    table += "<td>%s</td>" % p

                for i in self.colums:
                    table += "<td>%s</td>" % formatFields(item_dict, i, with_url=True)

            table += "</tr>"
        table += "</table><br>"

        self.url_type = []
        self.detail_type = None
        self.colums = None
        self.display_header = True
        self.unique_row = False

        return table


def render_toList(item_dict, show_colum, header_msg, detail_type=None):
    table = "<table id=\"customers_detail\">"
    return_link = ''
    if detail_type is not None:
        if detail_type == 'cliente':
            return_link += make_url('button', 'cliente', 'Ritorna al Cliente', '/anagrafe/%s/', cliente_id=item_dict['cliente_id'])
        elif detail_type == 'impianto':
            return_link += make_url('button', 'impianto', 'Ritorna all\'impianto', '/anagrafe/%s/impianto/%s/',
                    cliente_id=item_dict['cliente_id'], impianto_id=item_dict['impianto_id'])
        else:
            return_link = ''


    table += "<tr><th>%s</th><th>%s</th></tr>" % (return_link, header_msg)
    for i in show_colum:
        table += "<tr>"
        table += "<td class=\"hdr\">%s</td>" % i.replace('_', ' ').capitalize()
        table += "<td id=\"td_%s\">%s</td>" % (i, formatFields(item_dict, i, default_text="-"))
        table += "</tr>"

    table += "</table><br>"

    return table
