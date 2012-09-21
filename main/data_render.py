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
	'matricola_caldaia',
    'potenza_caldaia',
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
	'matricola_caldaia',
    'potenza_caldaia',
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

URL_CLIENTE = "<a href=\"/anagrafe/%s/%s\"><img src=\"/static/%s\" alt=\"%s\" title=\"%s\" width=\"%s\" height=\"%s\"/></a>"
URL_CLIENTE_ADD = "<a href=\"/anagrafe/%s\"><img src=\"/static/%s\" alt=\"%s\" title=\"%s\" width=\"%s\" height=\"%s\"/></a>"
URL_DETAIL = "<a href=\"/anagrafe/%s/%s/%s/%s\"><img src=\"/static/%s\" alt=\"%s\" title=\"%s\" width=\"%s\" height=\"%s\"/></a>"
URL_DETAIL_ADD = "<a href=\"/anagrafe/%s/%s/%s\"><img src=\"/static/%s\" alt=\"%s\" title=\"%s\" width=\"%s\" height=\"%s\"/></a>"
URL_SUB_DETAIL = "<a href=\"/anagrafe/%s/%s/%s/%s/%s\"><img src=\"/static/%s\" alt=\"%s\" title=\"%s\" width=\"%s\" height=\"%s\"/></a>"

class DataRender:
    def __init__(self, items, msg_items_empty = MSG_ITEMS_EMPTY):
        self.items = items
        self.colums = None
        self.display_header = True
        self.msg_items_empty = msg_items_empty
        self.url_type = []
        self.detail_type = None
        self.url_add = None
        self.select_record = None
        self.select_sub_record = None

    def showHeader(self, display_header):
        self.display_header = display_header

    def msgItemsEmpty(self, msg):
        self.msg_items_empty = msg

    def selectColums(self, colums):
        self.colums = colums

    def urlBarAdd(self, record_id, sub_record_id):
        self.url_add = ('add', 'plus.jpg', 'aggiungi..', 'aggiungi..', '16', '16')
        self.select_record = record_id
        self.select_sub_record = sub_record_id

    def urlBar(self, detail_type, url_type):
        self.detail_type = detail_type
        if 'edit' in url_type:
            self.url_type.append(('edit', 'edit.jpg', 'modifica..', 'modifica..', '16', '16'))
        if 'remove' in url_type:
            self.url_type.append(('delete', 'minus.jpg', 'cancella..', 'cancella..', '16', '16'))

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
                        p += URL_CLIENTE % ((item_dict['cliente_id'],) + j)
                    else:
                        p += URL_DETAIL % ((item_dict['cliente_id'], self.detail_type, item_dict[self.detail_type + '_id']) + j)

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

        if self.url_add is not None:
            table += "<h3>"
            if self.detail_type == 'cliente':
                table += URL_CLIENTE_ADD % (self.url_add)
            else:
                if self.detail_type == 'impianto':
                    table += URL_DETAIL_ADD % ((item_dict['cliente_id'], self.detail_type) + self.url_add)

                if self.detail_type in ['verifiche', 'intervento']:
                    table += URL_SUB_DETAIL % ((item_dict['cliente_id'], 'impianto', self.select_sub_record, self.detail_type) + self.url_add)

            table += " Aggiungi " + self.detail_type.capitalize()
            table += "</h3><br>"

        self.url_type = []
        self.url_add = None
        self.select_record = None
        self.select_sub_record = None
        self.detail_type = None
        self.colums = None

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
