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



ID_UNIQUE_CODE=30
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

    table_dict['data_ultima_analisi_combustione'] = row[ID_DATA_FUMI]
    table_dict['data_ultima_verifica'] = row[ID_DATA_VERIFICA]
    table_dict['data_prossima_analisi_combustione'] = row[ID_DATA_PROSSIMI_FUMI]
    table_dict['data_prossima_verifica'] = row[ID_DATA_PROSSIMA_VERIFICA]

    return table_dict

ID_DATA=19
ID_NUMERO_RAPPORTO=1
ID_TIPO_CONTROLLO=17
ID_COLORE_BOLLINO=22
ID_NUMERO_BOLLINO=23
ID_NOTE=29

def verifiche_csv(row):
    table_dict = {}

    table_dict['numero_rapporto'] = row[ID_NUMERO_RAPPORTO].strip()
    table_dict['tipo_verifica'] = row[ID_TIPO_CONTROLLO].capitalize().strip()
    d = data_fmt(row[ID_DATA])
    if d is not None:
        table_dict['data_verifica'] = d

    table_dict['colore_bollino'] = row[ID_COLORE_BOLLINO].capitalize().strip()

    n = row[ID_NUMERO_BOLLINO].strip()
    if n != "":
        n = int(n)
    else:
        n = None
    table_dict['numero_bollino'] = n
    table_dict['note_verifica'] = row[ID_NOTE]

    return table_dict

import models
from django.db import IntegrityError
#from django.db.models import Q

def load_csv(file_name):
    table = csv.reader(open(file_name, 'rb'), delimiter=',', quotechar='\"')
    data = ""
    row_dict = {}
    cli = None
    clienti_count = 0
    impianto_count = 0
    for row in table:
        d = cliente_csv(row)
        di = impianto_csv(row)
        dv = verifiche_csv(row)
        try:
            key = key2 = ""
            for i in d.values():
                if i != None:
                    key += "%s" % i

            for i in (di.values() + dv.values()):
                if i != None:
                    key2 += "%s" % i

        except KeyError, m:
            print row

        try:
            if key not in row_dict:
                cli = models.Cliente(**d)
                cli.save()
                row_dict[key] = cli
                clienti_count += 1

            if key2 not in row_dict:
                impianto_node = models.Impianto(cliente_impianto=row_dict[key], **di)
                impianto_node.save()
                row_dict[key2] = impianto_node

            verifica_node = models.Verifica(verifica_impianto=row_dict[key2], **dv)
            verifica_node.save()
            impianto_count += 1
        except IntegrityError, m:
            print row, m
            data +=  "%s %s %s %s\n" % (cli.pk, cli.nome, verifica_node.tipo_verifica_manutenzione, impianto_node.modello_caldaia)

    data += "Totale clienti %s, impianti %s\n" % (clienti_count, impianto_count)
    return data

def show_all_method():
    l = [(models.Cliente(),'main_cliente'),
         (models.Impianto(),'main_impianto'),
         (models.Verifica(),'main_verifica'),
         (models.Intervento(), 'main_intervento') ]

    print "(\\"
    for k in sorted(l):
        for i in k[0].__dict__.keys():
            if (i[0] != '_'):
                print "%s.%s \\\n" % (k[1], i),

    print ")"

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
