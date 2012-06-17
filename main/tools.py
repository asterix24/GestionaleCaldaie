#!/usr/bin/env python

#import clienti
import datetime
import csv

def data_fmt(s):
    if (s.strip() != ""):
        raw = s.replace(".", "/")
        print raw
        d, m, y = raw.split("/")
        return datetime.date(int(y), int(m), int(d))

    return None

def load_csv(file_name, handler):
    table = csv.reader(open(file_name, 'rb'), delimiter=',', quotechar='\"')
    all = []

    for e in table:
        try:
            if e != []:
                table_dict = handler(e)
        except (ValueError, IndexError, KeyError), m:
            print "ValueError (%s)" % m , e
            exit (0)

        all.append(table_dict)

    return all


def value_str(row, d, key):
    return row[d[key]]

cliente_csv_dict = {
    'cognome':1,
    'nome':2,
    'codice_fiscale':3,
    'via':4,
    'citta':5,
    'numero_telefono':7,
    'numero_cellulare':6,
    'mail':None
}


def cliente_csv(row):
    table_dict = {}
    cognome = value_str(row, cliente_csv_dict, 'cognome').capitalize().strip()
    if  cognome != '':
        table_dict['cognome'] = cognome

    nome = value_str(row, cliente_csv_dict, 'nome').capitalize().strip()
    if nome != '':
        table_dict['nome'] = nome

    cdf = value_str(row, cliente_csv_dict, 'codice_fiscale')
    if cdf.strip() != '':
        table_dict['codice_fiscale'] = cdf.upper().strip()

    table_dict['via'] = value_str(row, cliente_csv_dict, 'via').capitalize().strip()
    table_dict['citta'] = value_str(row, cliente_csv_dict, 'citta').capitalize().strip()

    cell = value_str(row, cliente_csv_dict, 'numero_cellulare')
    if cell.strip() != '':
        cell = cell.replace(' ', '')
    else:
        cell = "-"

    tel = value_str(row, cliente_csv_dict, 'numero_telefono')
    if tel.strip() != '':
        tel = tel.replace(' ', '')

        if tel[0] != '0':
            cell = tel
            tel = "-"
    else:
        tel = "-"

    table_dict['numero_telefono'] = tel
    table_dict['numero_cellulare'] = cell

    #table_dict['mail'] = None

    return table_dict


impianto_csv_dict = {
    'codice_id':0,
    'codice_impianto':None,
    'marca_caldaia':8,
    'modello_caldaia':10,
    'tipo':9,
    'combustibile':11,
    'data_installazione':12,
    'data_analisi_combustione':None,
    'data_contratto':13,
}

def impianto_csv(row):
    table_dict = {}

    id_imp = value_str(row, impianto_csv_dict, 'codice_id')
    if id_imp.strip() != '':
        table_dict['codice_id'] = id_imp

    #table_dict['codice_impianto'] = None
    table_dict['marca_caldaia'] = value_str(row, impianto_csv_dict, 'marca_caldaia').strip().upper()
    table_dict['tipo'] = value_str(row, impianto_csv_dict, 'tipo').strip().upper()
    table_dict['modello_caldaia'] = value_str(row, impianto_csv_dict, 'modello_caldaia').strip().upper()
    table_dict['combustibile'] = value_str(row, impianto_csv_dict, 'combustibile').strip().capitalize()
    table_dict['data_installazione'] = data_fmt(value_str(row, impianto_csv_dict, 'data_installazione'))
    table_dict['data_contratto'] = data_fmt(value_str(row, impianto_csv_dict, 'data_contratto'))

    return table_dict

verifiche_csv_dict = {
    'data':15,
    'tipo':None,
    'numerorapporto':None,
    'colore_bollino':16,
    'numero_bollino':18,
    'valore_bollino':17,
    'scadenza':None,
    'data_scadenza':None,
    'note':None
}

def verifiche_csv(row):
    table_dict = {}

    table_dict['tipo'] = 'analisi combustione'
    dt = value_str(row, verifiche_csv_dict, 'data').strip()
    if dt != "":
        dt = datetime.date(int(dt), 1, 1)
    else:
        dt = None
    table_dict['data'] = dt
    table_dict['colore_bollino'] = value_str(row, verifiche_csv_dict, 'colore_bollino').capitalize().strip()

    v = value_str(row, verifiche_csv_dict, 'valore_bollino').strip()
    if v == "":
        v = 0
    else:
        v = int(v)
    table_dict['valore_bollino'] = v

    n = value_str(row, verifiche_csv_dict, 'valore_bollino').strip()
    if n != "":
        n = int(n)
    else:
        n = 0
    table_dict['valore_bollino'] = n

    return table_dict

def load_all():
    x = load_csv("main/elenco2010.csv", cliente_csv)
    y = load_csv("main/elenco2010.csv", impianto_csv)
    z = load_csv("main/elenco2010.csv", verifiche_csv)

    for n,i in enumerate(x):
        k = dict(i.items() + y[n].items())
        j = dict(z[n].items() + k.items())
        for i in j.keys():
            print ("%s: %s") % (i, j[i])
	print

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
