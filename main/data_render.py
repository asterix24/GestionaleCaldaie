#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import models

from main import cfg

logger = logging.getLogger(__name__)

MSG_ITEMS_EMPTY = "<br><tr><h2>La ricerca non ha prodotto risultati</h2></tr><br>"
MSG_STATISTICS = "<br><tr><h2>Records trovati: %s</h2></tr><br>"
EMPTY_CELL = '<center>-</center>'
ACTION_DICT = {
        'add':'plus.jpg',
        'delete':'minus.jpg',
        'edit':'edit.jpg'
        }

CLIENTE_ID = 0
IMPIANTO_ID = 1
VERIFICA_ID = 2
INTERVENTO_ID = 3

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

    return make_url('','', items[key], '/anagrafe/%s/#cliente', items['cliente_id'])

def __impianto_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    return make_url('','', items[key], '/anagrafe/%s/impianto/%s/#impianto',
            items['cliente_id'], items['impianto_id'])

def __verifica_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return "Nessuna verifica"

    str = items[key]
    if type(str) == datetime.date:
        str = str.strftime(cfg.DATA_FIELD_STR_FORMAT)
    return make_url('','', str, '/anagrafe/%s/impianto/%s/verifica/%s/#verifica',
            items['cliente_id'], items['impianto_id'], items['verifica_id'])

def __ultima_analisi_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return "No Fumi"

    str = items[key]
    if type(str) == datetime.date:
        str = str.strftime(cfg.DATA_FIELD_STR_FORMAT)
    return make_url('','', str, '/anagrafe/%s/impianto/%s/verifica/%s/#verifica',
            items['cliente_id'], items['impianto_id'], items['ultima_analisi_combustione_id'])

def __stato_verifica_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    s = models.STATO_VERIFICA.get(items[key], s)
    return make_url('','', s, '/anagrafe/%s/impianto/%s/verifica/%s/#verifica',
            items['cliente_id'], items['impianto_id'], items['verifica_id'])

def __stato_impianto_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    return make_url('','', items[key], '/anagrafe/%s/impianto/%s/#impianto',
            items['cliente_id'], items['impianto_id'])

def __intervento_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    s = items[key].strftime(cfg.DATA_FIELD_STR_FORMAT)
    return make_url('','', s, '/anagrafe/%s/impianto/%s/intervento/%s/#intervento',
            items['cliente_id'], items['impianto_id'], items['intervento_id'])

def __tipo_intervento_url(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    return make_url('','', items[key], '/anagrafe/%s/impianto/%s/intervento/%s/#intervento',
            items['cliente_id'], items['impianto_id'], items['intervento_id'])

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
        if str in models.VERIFICHE_TYPE_CHOICES:
            s = models.VERIFICHE_TYPE_CHOICES[str]

    return s

def __colore_bollino(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    str = items[key]
    if str.lower() == 'altro':
        s = items['altro_colore_bollino']
    else:
        if str in models.BOLLINO_COLOR_CHOICES:
            s = models.BOLLINO_COLOR_CHOICES[str]

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

    return models.STATO_PAGAMENTO.get(items[key], s)


def __stato_impianto(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    return items[key]

def __anzianita_impianto(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    d = items[key]
    y = d.days / 365
    m = (d.days - (y * 365)) / 31
    d = (d.days - (y * 365)) - m * 31
    return "%s anni, %s mesi, %s giorni" % (y, m, d)

def __stato_verifica(items, key, s=EMPTY_CELL):
    if not isValidKey(items, key):
        return s

    return models.STATO_VERIFICA.get(items[key], s)

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
    'stato_verifica': __stato_verifica_url,
    'stato_impianto': __stato_impianto_url,
    'data_intervento': __intervento_url,
    'tipo_intervento': __tipo_intervento_url,
}

RENDER_TABLE = {
    'tipo_caldaia': __tipo_caldaia,
    'tipo_verifica': __tipo_verifica,
    'colore_bollino': __colore_bollino,
    'analisi_combustione': __analisi_combustione,
    'stato_pagamento': __stato_pagamento,
    'stato_impianto': __stato_impianto,
    'anzianita_impianto': __anzianita_impianto,
    'stato_verifica': __stato_verifica,
}

def formatFields(item_dict, field_name, with_url=False, default_text=EMPTY_CELL):
    try:
        s = default_text
        if item_dict.has_key(field_name):
            if with_url == False and field_name in RENDER_TABLE:
                s = RENDER_TABLE[field_name](item_dict, field_name, default_text)
            elif with_url and field_name in RENDER_TABLE_URL:
                s = RENDER_TABLE_URL[field_name](item_dict, field_name, default_text)
            else:
                s  = item_dict[field_name]
                if not isValidKey(item_dict, field_name):
                    s = default_text
                elif type(s) == datetime.date:
                    s = s.strftime(cfg.DATA_FIELD_STR_FORMAT)
        else:
            logger.error("Key not present %s" % (field_name))

    except (KeyError, ValueError), m:
        logger.error("%s Errore nel render di (%s) s=%s {%s}" % (__name__, m, s, item_dict))
        s = default_text

    return s


WIDGET_KEY = 0
WIDGET_LIST = 1

class DataRender(object):
    def __init__(self, items, msg_items_empty=MSG_ITEMS_EMPTY, show_statistics=False, msg_statistics=MSG_STATISTICS):
        self.items = items
        self.colums = None
        self.display_header = True
        self.msg_items_empty = msg_items_empty
        self.show_statistics = show_statistics
        self.msg_statistics = msg_statistics
        self.url_action = []
        self.detail_type = None
        self.url_add = None
        self.unique_row = False
        self.widget_list = []

        self.add_order_by_link = False
        self.base_url = ""
        self.string = ""

    def showHeader(self, display_header):
        self.display_header = display_header

    def uniqueRow(self):
        self.unique_row = True

    def msgItemsEmpty(self, msg):
        self.msg_items_empty = msg

    def showStatistics(self):
        self.show_statistics = True

    def msgStatistics(self, msg):
        self.msg_statistics = msg

    def selectColums(self, colums):
        self.colums = colums

    def actionWidget(self, detail_type, url_action):
        self.detail_type = detail_type
        self.url_action = url_action

    def menuWidget(self, widget_list):
        self.widget_list = widget_list

    def orderUrl(self, base_url, order_url_dict):
        self.add_order_by_link = True
        self.string = "?"
        self.base_url = base_url
        order = 'asc'
        for k,v in order_url_dict.items():
            if v is None:
                continue
            if k == 'ordering':
                continue
            if k == 'order_by_field':
                if not v:
                    continue

                if order_url_dict['ordering'] == 'asc':
                    order = 'desc'
                else:
                    order = 'asc'

                try:
                    _, field = v.split('.')
                    cfg.GROUP_FIELD_VIEW[field]['order'] = order
                except (ValueError, KeyError), m:
                    logger.error("%s Errore nello split di %s=%s" % (__name__, k, v))

                continue


            self.string += "%s=%s&" % (k, v)


    def toTable(self):
        if self.items == []:
            return self.msg_items_empty

        # Init table string
        table = ""

        # Show statistics of founded records
        if self.show_statistics:
            table += self.msg_statistics % len(self.items)
            self.show_statistics = False

        duplicate_row = {}
        cycle = False

        show_check = False
        for widget in self.widget_list:
            if widget[WIDGET_KEY] == 'check':
                show_check = True
                for i in widget[WIDGET_LIST]:
                    table += "<input type=\"button\" name=\"button_check\" value=\"%s\">" % i
            if widget[WIDGET_KEY] == 'button':
                for i in widget[WIDGET_LIST]:
                    table += "<input type=\"submit\" name=\"button_action\" value=\"%s\">" % i

        table += "<table id=\"customers\">"
        for item_dict in self.items:
            if self.display_header:
                table += "<tr>"

                if self.detail_type is not None or self.widget_list != []:
                    table += "<th></th>"

                for j in self.colums:
                    s = j.replace('_', ' ').capitalize()
                    if self.add_order_by_link:
                        if cfg.GROUP_FIELD_VIEW.has_key(j):
                            s = "<a class=\"table_header_%s\" href=\"/%s/%sorder_by_field=%s&ordering=%s\">%s</a>" % (cfg.GROUP_FIELD_VIEW[j]['order'],
                                    self.base_url, self.string, cfg.GROUP_FIELD_VIEW[j]['field'], cfg.GROUP_FIELD_VIEW[j]['order'], s)
                    table += "<th>%s</th>" % s

                table += "</tr>"
                self.display_header = False

            # To not display same row..
            skip_row = False
            if self.unique_row:
                key = ""
                for i in self.colums:
                    key += "%s" % item_dict.get(i,'')
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
                # Aggiustare quest blocco..
                if self.detail_type is not None or self.widget_list != []:
                    p = ''
                    if show_check:
                        cliente_id = item_dict.get('cliente_id', '')
                        impianto_id = item_dict.get('impianto_id', '')
                        verifica_id = item_dict.get('verifica_id', '')
                        intervento_id = item_dict.get('intervento_id', '')
                        p += "<input type=\"checkbox\" name=\"row_select\" value=\"%s,%s,%s,%s\">" % (cliente_id,
                                    impianto_id, verifica_id, intervento_id)
                    else:
                        for j in self.url_action:
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

        self.url_action = []
        self.detail_type = None
        self.colums = None
        self.display_header = True
        self.unique_row = False
        self.widget_list = []
        show_check = False

        self.add_order_by_link = False
        self.base_url = ""
        self.string = ""

        return table


def render_toList(item_dict, show_colum, header_msg, detail_type=None):
    table = "<table id=\"list_table\" class=\"list_table_float_left\">"
    table += "<colgroup><col width=50%><col width=50%></colgroup>"
    return_link = ''
    if detail_type is not None:
        if detail_type == 'cliente':
            return_link += make_url('button', 'cliente', 'Ritorna al Cliente', '/anagrafe/%s/#cliente', cliente_id=item_dict['cliente_id'])
        elif detail_type == 'impianto':
            return_link += make_url('button', 'impianto', 'Ritorna all\'impianto', '/anagrafe/%s/impianto/%s/#impianto',
                    cliente_id=item_dict['cliente_id'], impianto_id=item_dict['impianto_id'])
        else:
            return_link = ''


    table += "<tr><th>%s</th><th>%s</th></tr>" % (return_link, header_msg)
    for i in show_colum:
        table += "<tr>"
        table += "<td class=\"hdr\">%s</td>" % i.replace('_', ' ').capitalize()
        table += "<td id=\"td_%s\">%s</td>" % (i, formatFields(item_dict, i, default_text="-"))
        table += "</tr>"

    table += "</table>"

    return table

