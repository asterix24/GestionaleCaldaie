#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import models
import re
from functools import partial

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

    s = models.STATO_VERIFICA_DICT.get(items[key], s)
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
        if str in models.VERIFICHE_TYPE_CHOICES_DICT:
            s = models.VERIFICHE_TYPE_CHOICES_DICT[str]

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

    return models.STATO_PAGAMENTO_DICT.get(items[key], s)


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

    return models.STATO_VERIFICA_DICT.get(items[key], s)

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


def id_replace(m, item_dict):
    k = m.group()
    field_name = k[1:-1].lower()
    if field_name in ['cliente_id', 'impianto_id', 'verifica_id', 'intervento_id']:
        return str(item_dict.get(field_name,'noid'))
    else:
        return 'noid'

class DataRender(object):
    def __init__(self, items, msg_items_empty=MSG_ITEMS_EMPTY, show_statistics=False, msg_statistics=MSG_STATISTICS):
        self.items = items
        self.colums = None
        self.display_header = True
        self.msg_items_empty = msg_items_empty
        self.show_statistics = show_statistics
        self.msg_statistics = msg_statistics

        self.toolbar_top = []
        self.toolbar_left = []
        self.toolbar_bot  = []
        self.toolbar_last_row = []

        self.add_order_by_link = False
        self.base_url = ""
        self.string = ""
        self.selected_order_field = ""

    def showHeader(self, display_header):
        self.display_header = display_header

    def msgItemsEmpty(self, msg):
        self.msg_items_empty = msg

    def showStatistics(self):
        self.show_statistics = True

    def msgStatistics(self, msg):
        self.msg_statistics = msg

    def selectColums(self, colums):
        self.colums = colums

    def toolbar(self, top=[], left=[], last_row=[], bot=[]):
        for w in top:
            self.toolbar_top.append(w)
        for w in left:
            self.toolbar_left.append(w)
        for w in bot:
            self.toolbar_bot.append(w)
        for w in last_row:
            self.toolbar_last_row.append(w)

    def orderUrl(self, base_url, order_url_dict):
        self.add_order_by_link = True
        self.string = "?"
        self.base_url = base_url
        for k,v in order_url_dict.items():
            if v is None:
                continue
            if k == 'ordering':
                continue
            if k == 'order_by_field':
                if not v:
                    continue

                try:
                    _, field = v.split('.')
                    cfg.GROUP_FIELD_VIEW[field]['order'] = order_url_dict['ordering']
                    self.selected_order_field = field
                except (ValueError, KeyError), m:
                    logger.error("%s Errore nello split di %s=%s" % (__name__, k, v))

                continue

            self.string += "%s=%s&" % (k, v)


    def toTable(self):
        if self.items == []:
            return self.msg_items_empty

        # Init table string
        table = "<div>"

        # Show statistics of founded records
        if self.show_statistics:
            table += self.msg_statistics % len(self.items)
            self.show_statistics = False

        if self.toolbar_top:
            table += "<div class=\"btn-group\">"
            for t in self.toolbar_top:
                table += "%s" % re.sub('(<\w+>)', partial(id_replace, item_dict=self.items[0]), t)
            table += "</div>"

        table += "<table id=\"customers\" class=\"table table-striped table-hover table-condensed\">"
        if not self.items:
            table += "<thead><tr>"
            for j in self.colums:
                s = j.replace('_', ' ').capitalize()
                table += "<th>%s</th>" % s
            table += "</thead></tr>"

            table += "</td></tr>"

            colspan = len(self.colums) + 1
            table += "<tr><td colspan=\"%s\">" % colspan
            for t in self.toolbar_last_row:
                table += t
            table += "</td></tr>"


        else:
            for item_dict in self.items:
                if self.display_header:
                    table += "<thead><tr>"

                    if self.toolbar_left:
                        table += "<th></th>"

                    for j in self.colums:
                        table += "<th>%s</th>" % j.replace('_', ' ').capitalize()

                    table += "</tr><tr>"

                    if self.toolbar_left:
                        table += "<th></th>"

                    for j in self.colums:
                        if self.add_order_by_link:
                            if cfg.GROUP_FIELD_VIEW.has_key(j):
                                order_link_asc = "/%s/%sorder_by_field=%s&ordering=asc" % (self.base_url, self.string, cfg.GROUP_FIELD_VIEW[j]['field'])
                                order_link_desc = "/%s/%sorder_by_field=%s&ordering=desc" % (self.base_url, self.string, cfg.GROUP_FIELD_VIEW[j]['field'])
                                btn_state_asc = 'info'
                                btn_state_desc = 'info'
                                if j == self.selected_order_field:
                                    if cfg.GROUP_FIELD_VIEW[j]['order'] == 'asc':
                                        btn_state_asc = 'warning'
                                        btn_state_desc = 'info'
                                    else:
                                        btn_state_asc = 'info'
                                        btn_state_desc = 'warning'

                                table += """ <th> <div class="btn-group"> <a class="btn btn-mini btn-%s" href="%s"><i class="icon-chevron-up icon-white"></i></a> <a class="btn btn-mini btn-%s" href="%s"><i class="icon-chevron-down icon-white"></i></a> </div> </th> """ % (btn_state_asc, order_link_asc, btn_state_desc, order_link_desc)


                    table += "</tr></thead> <tbody>"
                    self.display_header = False


                table += "<tr>"

                if self.toolbar_left:
                    table += "<td>"
                    for t in self.toolbar_left:
                        table += "%s" % re.sub('(<\w+>)', partial(id_replace, item_dict=item_dict), t)
                    table += "</td>"

                for i in self.colums:
                    table += "<td>%s</td>" % formatFields(item_dict, i, with_url=True)

                table += "</tr>"

            if self.toolbar_last_row:
                colspan = len(self.colums) + 1
                table += "<tr><td colspan=\"%s\">" % colspan
                for t in self.toolbar_last_row:
                    table += "%s" % re.sub('(<\w+>)', partial(id_replace, item_dict=self.items[0]), t)

                table += "</td></tr>"

        table += "</tbody></table>"
        if self.toolbar_bot:
            for t in self.toolbar_bot:
                table += "%s" % re.sub('(<\w+>)', partial(id_replace, item_dict=item_dict), t)

        table += "</div>"

        self.colums = None
        self.display_header = True

        self.add_order_by_link = False
        self.base_url = ""
        self.string = ""

        return table


def render_toList(item_dict, show_colum, header_msg, detail_type=None, toolbar=[]):
    table = "<table id=\"list_table\" class=\"list_table_float_left\">"
    table += "<colgroup><col width=50%><col width=50%></colgroup>"

    cycle = False
    toolbar_t = ''
    for t in toolbar:
        toolbar_t += "%s" % re.sub('(<\w+>)', partial(id_replace, item_dict=item_dict), t)

    table += "<tr><th>%s</th><th>%s</th></tr>" % (toolbar_t, header_msg)
    for i in show_colum:
        cycle_str = ''
        if cycle:
            cycle_str = " class=\"alt\""
        cycle = not cycle

        table += "<tr %s>" % cycle_str
        table += "<td class=\"hdr\">%s</td>" % (i.replace('_', ' ').capitalize())
        table += "<td id=\"td_%s\">%s</td>" % (i, formatFields(item_dict, i, default_text="-"))
        table += "</tr>"

    table += "</table>"

    return table

