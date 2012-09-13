#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

ANAGRAFE_COLUM = [
	'cognome',
	'nome',
	'codice_fiscale',
	'via',
	'citta',
	'numero_telefono',
	'numero_cellulare',
	'mail',
	'codice_impianto',
	'marca_caldaia',
	'modello_caldaia',
	'tipo_caldaia',
	'combustibile',
	'data_installazione',
	'data_analisi_combustione',
	'data_contratto',
	'colore_bollino',
	'data_scadenza',
	]

SCHEDA_ANAGRAFE = [
	'cognome',
	'nome',
	'codice_fiscale',
	'via',
	'citta',
	'numero_telefono',
	'numero_cellulare',
	'mail'
	]

SCHEDA_ANAGRAFE_IMPIANTI = [
	'codice_impianto',
	'marca_caldaia',
	'modello_caldaia',
	'tipo_caldaia',
	'combustibile',
	'data_installazione',
	'data_analisi_combustione',
	'data_contratto',
	]

SCHEDA_ANAGRAFE_VERIFICHE = [
	'data_verifica_manutenzione',
	'tipo_verifica_manutenzione',
	'numero_rapporto',
	'colore_bollino',
	'numero_bollino',
	'valore_bollino',
	'scadenza',
	'data_scadenza',
	]

SCHEDA_ANAGRAFE_INTERVENTI = [
	'note_verifiche_manutenzione',
	'data_intervento',
	'tipo_intervento',
	'note_intervento',
	]


SHOW_ALL_COLUM=[
	'cliente_data_inserimento',
	'cognome',
	'nome',
	'codice_fiscale',
	'via',
	'citta',
	'numero_telefono',
	'numero_cellulare',
	'mail',
	'impianto_data_inserimento',
	'codice_id',
	'codice_impianto',
	'marca_caldaia',
	'modello_caldaia',
	'tipo_caldaia',
	'combustibile',
	'data_installazione',
	'data_analisi_combustione',
	'data_contratto',
	'data_verifica_manutenzione',
	'tipo_verifica_manutenzione',
	'numero_rapporto',
	'colore_bollino',
	'numero_bollino',
	'valore_bollino',
	'scadenza',
	'data_scadenza',
	'note_verifiche_manutenzione',
	'data_intervento',
	'tipo_intervento',
	'note_intervento',
	]

DATA_FIELD_STR_FORMAT = "%d/%m/%Y"
ANAGRAFE_DETAILS_URL = "\"/anagrafe/%s/\""
IMPIANTO_DETAILS_URL = "\"/anagrafe/%s/impianto/%s/\""
VERIFICHE_DETAILS_URL = "\"/anagrafe/%s/verifiche/%s/\""

MSG_ITEMS_EMPTY = "<br><tr><h2>La ricerca non ha prodotto risultati</h2></tr><br>"

URL_TEMPLATE = "<a href=\"/anagrafe/%s/%s/%s/%s\"><img src=\"/static/%s\" alt=\"%s\" title=\"%s\" width=\"%s\" height=\"%s\" /></a>"

class DataRender:
    def __init__(self, items, msg_items_empty = MSG_ITEMS_EMPTY):
        self.items = items
        self.colums = None
        self.display_header = True
        self.msg_items_empty = msg_items_empty
        self.url_type = None
        self.detail_type = None

    def showHeader(self, display_header):
        self.display_header = display_header

    def msgItemsEmpty(self, msg):
        self.msg_items_empty = msg

    def selectColums(self, colums):
        self.colums = colums

    def urlBar(self, detail_type, url_type):
        if url_type == 'edit':
            self.url_type = ('edit', 'edit.jpg', 'modifica..', 'modifica..', '16', '16')
        elif url_type == 'remove':
            self.url_type = ('delete', 'minus.jpg', 'cancella..', 'cancella..', '16', '16')
        elif url_type == 'add':
            self.url_type = ('add', 'plus.jpg', 'cancella..', 'cancella..', '16', '16')
        else:
            self.url_type = None

        self.detail_type = detail_type

    def toTable(self):
        if self.items == []:
            return msg_items_empty

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
                p = URL_TEMPLATE % ((item_dict['cliente_id'], self.detail_type, item_dict[self.detail_type + '_id']) + self.url_type)
                table += "<td>%s</td>" % p

            for i in self.colums:
                try:
                    s  = item_dict[i]
                    if type(s) == datetime.date:
                        s = s.strftime(DATA_FIELD_STR_FORMAT)
                    if i in ['nome', 'cognome']:
                        s = '<a href=%s>%s</a>' % ((ANAGRAFE_DETAILS_URL % item_dict['cliente_id']), s)
                    if i in ['codice_impianto', 'marca_caldaia'] and s is not None:
                        s = '<a href=%s>%s</a>' % ((IMPIANTO_DETAILS_URL % (item_dict['cliente_id'], item_dict['impianto_id'])), s)
                    if i == 'data_verifica_manutenzione':
                        s = '<a href=%s>%s</a>' % ((VERIFICHE_DETAILS_URL % (item_dict['cliente_id'], item_dict['verifiche_id'])), s)
                    if s is None:
                        s = '-'
                except (KeyError, ValueError), m:
                    print "Errore nel render di %s (%s)" % (i, m)
                    s = '-'
                table += "<td>%s</td>" % s

            table += "</tr>"
        table += "</table>"

        self.url_type = None
        self.detail_type = None
        self.colums = None

        return table


def render_toTable(items, show_colum, display_header=True, no_items_msg=MSG_ITEMS_EMPTY, decorator=None):
    if items == []:
        return no_items_msg

    cycle = False
    table = "<table id=\"customers\">"
    for item_dict in items:
        if display_header:
            table += "<tr>"
            table += "<th></th>"
            for j in show_colum:
                table += "<th>%s</th>" % j.replace('_', ' ').capitalize()
            table += "</tr>"
            display_header = False

        cycle_str = ''
        if cycle:
            cycle_str = " class=\"alt\""
        cycle = not cycle

        table += "<tr%s>" % cycle_str
        if decorator is not None:
            table += "<td>%s</td>" % decorator
        for i in show_colum:
            try:
                s  = item_dict[i]
                if type(s) == datetime.date:
                    s = s.strftime(DATA_FIELD_STR_FORMAT)
                if i in ['nome', 'cognome']:
                    s = '<a href=%s>%s</a>' % ((ANAGRAFE_DETAILS_URL % item_dict['cliente_id']), s)
                if i in ['codice_impianto', 'marca_caldaia'] and s is not None:
                    s = '<a href=%s>%s</a>' % ((IMPIANTO_DETAILS_URL % (item_dict['cliente_id'], item_dict['impianto_id'])), s)
                if i == 'data_verifica_manutenzione':
                    s = '<a href=%s>%s</a>' % ((VERIFICHE_DETAILS_URL % (item_dict['cliente_id'], item_dict['verifiche_id'])), s)	
                if s is None:
                    s = '-'
            except (KeyError, ValueError), m:
                print "Errore nel render di %s (%s)" % (i, m)
                s = '-'
            table += "<td>%s</td>" % s
        table += "</tr>"
    table += "</table>"

    return table


def render_toList(item_dict, show_colum, header_msg):
	table = "<table id=\"customers_detail\">"
	table += "<tr><th></th><th>%s</th></tr>" % header_msg
	for i in show_colum:
		try:
			table += "<tr>"
			table += "<td class=\"hdr\">%s</td>" % i.replace('_', ' ').capitalize()
			s  = item_dict[i]
			if s is None:
				s = '-'
			elif type(s) == datetime.date:
				s = s.strftime(DATA_FIELD_STR_FORMAT)

		except (KeyError, ValueError), m:
			print "Errore nel render di %s (%s)" % (i, m)
			s = '-'

		table += "<td>%s</td>" % s
		table += "</tr>"

	table += "</table>"

	return table
