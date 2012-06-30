#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import csv

def data_fmt(s):
	if (s.strip() != ""):
		raw = s.replace(".", "/")
		d, m, y = raw.split("/")
		return datetime.date(int(y), int(m), int(d))

	return None

def load_csv(file_name, handler):
	table = csv.reader(open(file_name, 'rb'), delimiter=',', quotechar='\"')
	all = []

	for e in table:
		#try:
		if e != []:
			table_dict = handler(e)
		#except (ValueError, IndexError, KeyError), m:
		#    print "ValueError (%s)" % m , e
		#    exit (0)

		all.append(table_dict)

	return all

# Cliente
ID_COGNOME=1
ID_NOME=2
ID_CODICE_FISCALE=3
ID_VIA=4
ID_CITTA=5
ID_NUMERO_TELEFONO=7
ID_NUMERO_CELLULARE=6

def cliente_csv(row):
	table_dict = {}
	cognome = row[ID_COGNOME].capitalize().strip()
	if  cognome != '':
		table_dict['cognome'] = cognome

	nome = row[ID_NOME].capitalize().strip()
	if nome != '':
		table_dict['nome'] = nome

	cdf = row[ID_CODICE_FISCALE]
	if cdf.strip() != '':
		table_dict['codice_fiscale'] = cdf.upper().strip()

	table_dict['via'] =  row[ID_VIA].capitalize().strip()
	table_dict['citta'] = row[ID_CITTA].capitalize().strip()

	cell = row[ID_NUMERO_CELLULARE]
	if cell.strip() != '':
		cell = cell.replace(' ', '')
	else:
		cell = None

	tel = row[ID_NUMERO_TELEFONO]
	if tel.strip() != '':
		tel = tel.replace(' ', '')

		if tel[0] != '0':
			cell = tel
			tel = None
	else:
		tel = None

	table_dict['numero_telefono'] = tel
	table_dict['numero_cellulare'] = cell

	return table_dict


ID_CODICE_ID=0
ID_MARCA_CALDAIA=8
ID_MODELLO_CALDAIA=10
ID_TIPO=9
ID_COMBUSTIBILE=11
ID_DATA_INSTALLAZIONE=12
ID_DATA_CONTRATTO=13

def impianto_csv(row):
	table_dict = {}
	id_imp = row[ID_CODICE_ID]

	if id_imp.strip() != '':
		table_dict['codice_id'] = id_imp

	table_dict['marca_caldaia'] = row[ID_MARCA_CALDAIA].strip().upper()
	table_dict['tipo_caldaia'] = row[ID_TIPO].strip().upper()
	table_dict['modello_caldaia'] = row[ID_MODELLO_CALDAIA].strip().upper()
	table_dict['combustibile'] = row[ID_COMBUSTIBILE].strip().capitalize()

	table_dict['data_installazione'] = data_fmt(row[ID_DATA_INSTALLAZIONE])
	table_dict['data_contratto'] = data_fmt(row[ID_DATA_CONTRATTO])

	return table_dict

ID_DATA=15
ID_COLORE_BOLLINO=16
ID_NUMERO_BOLLINO=18
ID_VALORE_BOLLINO=17

def verifiche_csv(row):
	table_dict = {}

	table_dict['tipo_verifica_manutenzione'] = 'analisi combustione'

	dt = row[ID_DATA].strip()
	if dt != "":
		dt = datetime.date(int(dt), 1, 1)
	else:
		dt = datetime.date.today()
	table_dict['data_verifica_manutenzione'] = dt

	table_dict['colore_bollino'] = row[ID_COLORE_BOLLINO].capitalize().strip()

	v = row[ID_VALORE_BOLLINO].strip()
	if v == "":
		v = 0
	else:
		v = int(v)
	table_dict['valore_bollino'] = v

	n = row[ID_NUMERO_BOLLINO].strip()
	if n != "":
		n = int(n)
	else:
		n = None
	table_dict['numero_bollino'] = n

	return table_dict

import models
from django.db import IntegrityError
from django.db.models import Q

def insert_csv_files():
	cliente_dict = load_csv("main/elenco2010.csv", cliente_csv)
	impianto_dict = load_csv("main/elenco2010.csv", impianto_csv)
	verifiche_dict = load_csv("main/elenco2010.csv", verifiche_csv)

	index = 0
	clienti_count = 0
	for index, item in enumerate(cliente_dict):
		cli = models.Cliente(**item)
		try:
			s = cli.save()
			clienti_count += 1
		except IntegrityError, m:
			cli_search = models.Cliente.objects.filter(cognome__iexact = item['cognome'])
			try:
				if item['nome'] is not None:
					cli_search = cli_search.filter(nome__iexact = item['nome'])
			except KeyError, m:
				print item, m

			if len(cli_search) >= 1:
				cli = cli_search[0]

			print "Skip %d %s (%s)" % (index, cli.nome, m)

		try:
			impianto_node = models.Impianto(cliente_impianto = cli, **impianto_dict[index])
			impianto_node.save()
		except IntegrityError, m:
			impianto_search = models.Impianto.objects.filter(marca_caldaia__iexact = impianto_dict[index]['marca_caldaia'])
			impianto_search = impianto_search.filter(modello_caldaia__iexact = impianto_dict[index]['modello_caldaia'])
			impianto_search = impianto_search.filter(data_installazione__iexact = impianto_dict[index]['data_installazione'])

			try:
				if item['codice_id'] is not None:
					cli_search = cli_search.filter(codice_id__iexact = impianto_dict[index]['codice_id'])
			except KeyError, m:
				print item, m

			if len(cli_search) >= 1:
				impianto_node = impianto_search[0]

			print "%d %s skipped.. (%s)" % (index, impianto_node.modello_caldaia, m)

		verifiche_node = models.VerificheManutenzione(verifiche_impianto = impianto_node, **verifiche_dict[index])
		verifiche_node.save()

		print "Ok", cli.pk, cli.nome, verifiche_node.tipo_verifica_manutenzione, impianto_node.modello_caldaia, "Row: ", index

	print "Record inseriti: %s, record totoali: %s" % (clienti_count, index)

def dump(l, key = None):
	if key is not None:
		print l[key]
	else:
		for i in l.keys():
			print ("%s: %s") % (i, l[i])

		print

def dump_all(l, key = None):
	for i in l:
		dump(i, key)

if __name__ == "__main__":
	import sys

	load_all()
	exit (1)

	if len(sys.argv) < 2:
		print sys.argv[0], " <csv file name>"
		exit (1)

	all = load_csv(sys.argv[1], load_cliente)
	print all

	print "Records: ", len(all)
