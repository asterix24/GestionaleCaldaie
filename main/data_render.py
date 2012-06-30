#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

def render_toTable(items, display_header=True, show_colum=SHOW_ALL_COLUM):
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
				if s is None:
					s = '-'
				elif i in ['nome', 'cognome']:
					s = '<a href=\"/anagrafe/%s/detail/\">%s</a>' % (item_dict['id'], s)
			except KeyError, m:
				s = '-'

			table += "<td>%s</td>" % s

		table += "</tr>"
	table += "</table>"

	return table
