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

        return datetime.date(int(y), int(m), int(d))

    return None

# Cliente
ID_COGNOME=5
ID_NOME=6
ID_CODICE_FISCALE=7
ID_VIA=8
ID_CITTA=9
ID_NUMERO_TELEFONO=10
ID_NUMERO_CELLULARE=11
ID_MAIL=12

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


ID_MARCA_CALDAIA=13
ID_TIPO=14
ID_MODELLO_CALDAIA=15
ID_MATRICOLA=16
ID_POTENZA=17
ID_COMBUSTIBILE=18
ID_DATA_INSTALLAZIONE=19
ID_CODICE_IMPIANTO=0

def impianto_csv(row):
    table_dict = {}

    table_dict['marca_caldaia'] = row[ID_MARCA_CALDAIA].strip().upper()
    table_dict['tipo_caldaia'] = row[ID_TIPO].strip().upper()
    table_dict['modello_caldaia'] = row[ID_MODELLO_CALDAIA].strip().upper()
    table_dict['matricola_caldaia'] = row[ID_MATRICOLA].strip().upper()
    combustibile = row[ID_COMBUSTIBILE].strip().capitalize()
    if combustibile.lower() == 'met':
        table_dict['combustibile'] = 'Metano'

    table_dict['potenza_caldaia'] = row[ID_POTENZA].strip().capitalize()

    table_dict['data_installazione'] = data_fmt(row[ID_DATA_INSTALLAZIONE])
    table_dict['codice_impianto'] = row[ID_CODICE_IMPIANTO].strip().capitalize()

    return table_dict

ID_NUMERO_RAPPORTO=1
ID_COLORE_BOLLINO=29
ID_NUMERO_BOLLINO=30
ID_NOTE=36
ID_DATA_FUMI=20
ID_DATA_VERIFICA=23
ID_TIPO_CONTROLLO=26

def verifiche_csv(row):
    table_dict = {}

    data_verifica = data_fmt(row[ID_DATA_FUMI])
    if data_verifica != None:
        table_dict['data_verifica'] = data_verifica
        table_dict['tipo_verifica'] = 'programmata'
        table_dict['numero_rapporto'] = row[ID_NUMERO_RAPPORTO].strip()

        #table_dict['codice_id']
        table_dict['prossima_verifica'] = data_verifica   + datetime.timedelta(days=365)

        if row[ID_TIPO_CONTROLLO].lower() == 'fumi':
            table_dict['analisi_combustione'] = True

            color = row[ID_COLORE_BOLLINO].capitalize().strip()
            if color == 'BLU':
                color = 'blu'
            if color == 'VER':
                color = 'verde'
            elif color == 'ARA':
                color = 'arancione'
            elif color == 'Gia':
                color = 'giallo'
            elif color == 'Si':
                color = 'blu'
            else:
                color = 'no'

            table_dict['colore_bollino'] = color

            if table_dict['colore_bollino'] == 'blu':
                table_dict['prossima_analisi_combustione'] = data_fmt(row[ID_DATA_FUMI]) + datetime.timedelta(days=365) * 2
            elif table_dict['colore_bollino'] == 'arancione':
                table_dict['prossima_analisi_combustione'] = data_fmt(row[ID_DATA_FUMI]) + datetime.timedelta(days=365)

            n = row[ID_NUMERO_BOLLINO].strip()
            if n != "":
                n = int(n)
            else:
                n = None

            table_dict['numero_bollino'] = n

        #table_dict['valore_bollino']
        #table_dict['stato_pagamento']
        #table_dict['costo_intervento']
        table_dict['note_verifica'] = row[ID_NOTE]
    else:
        print "Conversione errata: ", row[ID_DATA_FUMI]

    return table_dict

import models
from django.db import IntegrityError

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
            data +=  "%s %s %s\n" % (cli.pk, cli.nome, impianto_node.modello_caldaia)

    data += "Totale clienti %s, impianti %s\n" % (clienti_count, impianto_count)
    return data

models_list = {'main_cliente': models.Cliente(),
        'main_impianto': models.Impianto(),
        'main_verifica': models.Verifica(),
        'main_intervento': models.Intervento()}

def dbColumList(model_type=None):
    l = []
    if (model_type is not None) and (model_type in models_list.keys()):
        for i in models_list[model_type].__dict__.keys():
            if (i[0] != '_') and ('id' not in i):
                l.append(i)
    else:
        for k in sorted(models_list.values()):
            for i in k.__dict__.keys():
                if (i[0] != '_') and ('id' not in i):
                    l.append(i)
    return l

def show_all_method():
    print "(\\"
    for k in sorted(models_list.keys()):
        for i in models_list[k].__dict__.keys():
            if (i[1] != '_'):
                print "%s.%s \\\n" % (k, i),

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
