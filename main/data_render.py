#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import models

logger = logging.getLogger(__name__)

DATA_FIELD_STR_FORMAT = "%d/%m/%Y"
MSG_ITEMS_EMPTY = "<br><tr><h2>La ricerca non ha prodotto risultati</h2></tr><br>"
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
    url += "\">"

    if type == 'icon':
        data += "<img src=\"/static/%s\" alt=\"%s..\" title=\"%s..\" width=\"16\" height=\"16\"/> " % (ACTION_DICT[action], action, action)

    data += "%s"  % message
    return url + data + "</a>"

class DataRender(object):
    def __init__(self, items, msg_items_empty = MSG_ITEMS_EMPTY):
        self.items = items
        self.colums = None
        self.display_header = True
        self.msg_items_empty = msg_items_empty
        self.url_type = []
        self.detail_type = None
        self.url_add = None

    def showHeader(self, display_header):
        self.display_header = display_header

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
                try:
                    s  = item_dict[i]
                    if s is None or s == "":
                        s = '<center>-</center>'

                    elif type(s) == datetime.date:
                        s = s.strftime(DATA_FIELD_STR_FORMAT)
                        if i in ['data_verifica', 'ultima_verifica']:
                            s = make_url('','', s, '/anagrafe/%s/impianto/%s/verifica/%s/',
                                    item_dict['cliente_id'], item_dict['impianto_id'], item_dict['verifica_id'])

                    elif i in ['nome', 'cognome']:
                        s = make_url('','', s, '/anagrafe/%s/', item_dict['cliente_id'])

                    elif i in ['codice_impianto', 'marca_caldaia']:
                        s = make_url('','', s, '/anagrafe/%s/impianto/%s/', item_dict['cliente_id'], item_dict['impianto_id'])

                    elif i in ['stato_pagamento']:
                        if s:
                            s = "Pagato!"
                        else:
                            s = "Da riscuotere."

                    elif i in ['tipo_verifica']:
                        if s == "altro":
                           s = item_dict['altro_tipo_verifica']
                        else:
                            s = models.VERIFICHE_TYPE_CHOISES_DICT[s]

                    elif i in ['colore_bollino']:
                        if s in models.BOLLINO_COLOR_CHOICES_DICT.keys():
                            s = models.BOLLINO_COLOR_CHOICES_DICT[s]

                except (KeyError, ValueError), m:
                    print "Table Errore nel render di %s (%s) s=%s" % (i, m, s)
                    s = '<center>-</center>'

                table += "<td>%s</td>" % s

            table += "</tr>"
        table += "</table><br>"

        self.url_type = []
        self.detail_type = None
        self.colums = None
        self.display_header = True

        return table


def render_toList(item_dict, show_colum, header_msg, detail_type=None):
    table = "<table id=\"customers_detail\">"
    return_link = ''
    if detail_type is not None:
        if detail_type == 'cliente':
            return_link += make_url('', 'cliente', 'Ritorna al Cliente', '/anagrafe/%s/', cliente_id=item_dict['cliente_id'])
        elif detail_type == 'impianto':
            return_link += make_url('', 'impianto', 'Ritorna all\'impianto', '/anagrafe/%s/impianto/%s/',
                    cliente_id=item_dict['cliente_id'], impianto_id=item_dict['impianto_id'])
        else:
            return_link = ''


    table += "<tr><th>%s</th><th>%s</th></tr>" % (return_link, header_msg)
    for i in show_colum:
        try:
            table += "<tr>"
            table += "<td class=\"hdr\">%s</td>" % i.replace('_', ' ').capitalize()

            s  = item_dict[i]
            if s is None:
                s = '-'

            elif i in ['tipo_verifica']:
                if s == "altro":
                   s = item_dict['altro_tipo_verifica']
                else:
                    s = models.VERIFICHE_TYPE_CHOISES_DICT[s]

            elif i in ['colore_bollino']:
                if s in models.BOLLINO_COLOR_CHOICES_DICT.keys():
                    s = models.BOLLINO_COLOR_CHOICES_DICT[s]

            elif i in ['analisi_combustione']:
                if s:
                    s = "Si"
                else:
                    s = "No"

            elif i in ['stato_pagamento']:
                if s:
                    s = "Pagato!"
                else:
                    s = "Da riscuotere."

            elif type(s) == datetime.date:
                s = s.strftime(DATA_FIELD_STR_FORMAT)

        except (KeyError, ValueError), m:
            print "List Errore nel render di %s (%s)" % (i, m)
            s = '-'

        table += "<td id=\"td_%s\">%s</td>" % (i, s)
        table += "</tr>"

    table += "</table><br>"

    return table
