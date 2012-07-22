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

def render_toTable(items, show_colum, display_header=True, no_items_msg=MSG_ITEMS_EMPTY):
	if items == []:
		return no_items_msg
		
	cycle = False
	table = "<table id=\"customers\">"
	for item_dict in items:
		if display_header:
			table += "<tr>"
			for j in show_colum:
				table += "<th>%s</th>" % j.replace('_', ' ').capitalize()
			table += "</tr>"
			display_header = False

		cycle_str = ''
		if cycle:
			cycle_str = " class=\"alt\""
		cycle = not cycle

		table += "<tr%s>" % cycle_str

		for i in show_colum:
			try:
				s  = item_dict[i]
				if type(s) == datetime.date:
					s = s.strftime(DATA_FIELD_STR_FORMAT)
				if s is None:
					s = '-'
				if i in ['nome', 'cognome']:
					s = '<a href=%s>%s</a>' % ((ANAGRAFE_DETAILS_URL % item_dict['cliente_id']), s)
				if i == 'codice_impianto':
					s = '<a href=%s>%s</a>' % ((IMPIANTO_DETAILS_URL % (item_dict['cliente_id'], item_dict['impianto_id'])), s)
				if i == 'data_verifica_manutenzione':
					s = '<a href=%s>%s</a>' % ((VERIFICHE_DETAILS_URL % (item_dict['cliente_id'], item_dict['verifiche_id'])), s)
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
