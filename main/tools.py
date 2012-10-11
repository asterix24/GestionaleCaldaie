#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import csv

def data_fmt(s):
    if (s.strip() != ""):
        raw = s.replace(".", "/")
        try:
            d, m, y = raw.split("/")
        except ValueError, m:
            print raw, m
            return None

        return datetime.date(int(y) + 2000, int(m), int(d))

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
ID_COGNOME=2
ID_NOME=3
ID_CODICE_FISCALE=4
ID_VIA=5
ID_CITTA=6
ID_NUMERO_TELEFONO=7
ID_NUMERO_CELLULARE=8
ID_MAIL=9

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

	table_dict['mail'] = row[ID_MAIL].capitalize().strip()

	return table_dict


ID_MARCA_CALDAIA=10
ID_TIPO=11
ID_MODELLO_CALDAIA=12
ID_MATRICOLA=13
ID_POTENZA=14
ID_COMBUSTIBILE=15
ID_DATA_INSTALLAZIONE=16
ID_CODICE_IMPIANTO=0
ID_DATA_FUMI=18
ID_DATA_PROSSIMI_FUMI=21
ID_DATA_VERIFICA=19
ID_DATA_PROSSIMA_VERIFICA=20

def impianto_csv(row):
    table_dict = {}

    table_dict['codice_id'] = row[ID_CODICE_IMPIANTO]
    table_dict['marca_caldaia'] = row[ID_MARCA_CALDAIA].strip().upper()
    table_dict['tipo_caldaia'] = row[ID_TIPO].strip().upper()
    table_dict['modello_caldaia'] = row[ID_MODELLO_CALDAIA].strip().upper()
    table_dict['matricola_caldaia'] = row[ID_MATRICOLA].strip().upper()
    table_dict['combustibile'] = row[ID_COMBUSTIBILE].strip().capitalize()
    table_dict['potenza_caldaia'] = row[ID_POTENZA].strip().capitalize()

    table_dict['data_installazione'] = data_fmt(row[ID_DATA_INSTALLAZIONE])
    table_dict['codice_impianto'] = row[ID_CODICE_IMPIANTO].strip().capitalize()

    table_dict['data_ultima_analisi_combustione'] = data_fmt(row[ID_DATA_FUMI])
    table_dict['data_ultima_verifica'] = data_fmt(row[ID_DATA_VERIFICA])
    table_dict['data_prossima_analisi_combustione'] = row[ID_DATA_PROSSIMI_FUMI]
    table_dict['data_prossima_verifica'] = row[ID_DATA_PROSSIMA_VERIFICA]

    return table_dict

ID_DATA=19
ID_TIPO_CONTROLLO=17
ID_COLORE_BOLLINO=22
ID_NUMERO_BOLLINO=23
ID_NOTE=29

def verifiche_csv(row):
	table_dict = {}

	table_dict['tipo_verifica_manutenzione'] = row[ID_TIPO_CONTROLLO].capitalize().strip()
	table_dict['data_verifica_manutenzione'] = data_fmt(row[ID_DATA])

	table_dict['colore_bollino'] = row[ID_COLORE_BOLLINO].capitalize().strip()

	n = row[ID_NUMERO_BOLLINO].strip()
	if n != "":
		n = int(n)
	else:
		n = None
	table_dict['numero_bollino'] = n
	table_dict['note_verifiche_manutenzione'] = row[ID_NOTE]

	return table_dict

import models
from django.db import IntegrityError
from django.db.models import Q

def insert_csv_files(cli_on = True):
    try:
        cliente_dict = load_csv("main/elenco2011.csv", cliente_csv)
        impianto_dict = load_csv("main/elenco2011.csv", impianto_csv)
        verifiche_dict = load_csv("main/elenco2011.csv", verifiche_csv)

        data = ""
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
                    if cli_on:
                        print  "Error", item, m
                    else:
                        data += "Error %s %s\n" % (item, m)

                if len(cli_search) >= 1:
                    cli = cli_search[0]

                if cli_on:
                    print "Skip %d %s (%s)" % (index, cli.nome, m)
                else:
                    data += "Skip %d %s (%s)\n" % (index, cli.nome, m)

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
                    if cli_on:
                        print item, m
                    else:
                        data += "Error %s %s" % (item, m)


                if len(cli_search) >= 1:
                    impianto_node = impianto_search[0]

                if cli_on:
                    print "%d %s skipped.. (%s)" % (index, impianto_node.modello_caldaia, m)
                else:
                    data += "%d %s skipped.. (%s)\n" % (index, impianto_node.modello_caldaia, m)

            verifiche_node = models.VerificheManutenzione(verifiche_impianto = impianto_node, **verifiche_dict[index])
            verifiche_node.save()

            if cli_on:
                print "Ok", cli.pk, cli.nome, verifiche_node.tipo_verifica_manutenzione, impianto_node.modello_caldaia, "Row: ", index
            else:
                data +=  "Ok %s %s %s %s Row: %s\n" % (cli.pk, cli.nome, verifiche_node.tipo_verifica_manutenzione, impianto_node.modello_caldaia, index)
    except IndexError, m:
        print "Errore:", m

    if cli_on:
        print "Record inseriti: %s, record totoali: %s" % (clienti_count, index)
    else:
        data += "Record inseriti: %s, record totoali: %s\n" % (clienti_count, index)
        return data

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
