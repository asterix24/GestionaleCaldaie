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

class DataRender:
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
                    if type(s) == datetime.date:
                        s = s.strftime(DATA_FIELD_STR_FORMAT)
                    if i in ['nome', 'cognome']:
                        s = make_url('','', s, '/anagrafe/%s/', item_dict['cliente_id'])
                    if i in ['codice_impianto', 'marca_caldaia'] and s is not None:
                        s = make_url('','', s, '/anagrafe/%s/impianto/%s/', item_dict['cliente_id'], item_dict['impianto_id'])
                    if i == 'data_verifica_manutenzione':
                        s = make_url('','', s, '/anagrafe/%s/impianto/%s/verifiche/%s/',
                                item_dict['cliente_id'], item_dict['impianto_id'], item_dict['verifiche_id'])
                    if s is None:
                        s = '-'
                except (KeyError, ValueError), m:
                    print "Errore nel render di %s (%s)" % (i, m)
                    s = '-'
                table += "<td>%s</td>" % s

            table += "</tr>"
        table += "</table>"

        self.url_type = []
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
