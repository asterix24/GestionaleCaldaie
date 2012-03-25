#!/usr/bin/env python

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
        try:
        	table_dict = handler(e)
        except ValueError, m:
            print "ValueError (%s)" % m , e
            exit (0)

        all.append(table_dict)

    return all

def load_intervento(e):
    d = {}
    print e
    d['cognome'] = e[0].capitalize().strip()
    d['nome'] = e[1].capitalize().strip()

    d['data'] = data_fmt(e[2])
    d['tipo'] = e[3].strip()
    d['numero_rapporto'] = int(e[4].strip())
    d['scadenza'] = int(e[5].strip())
    d['data_scadenza'] = data_fmt(e[6])
    d['note'] = e[7]

def load_bollino(e):
    d = {}
    print e
    d['cognome'] = e[0].capitalize().strip()
    d['nome'] = e[1].capitalize().strip()

    p = 0
    if e[2].lower() == 'si':
        p = 1
    d['presente'] = p
    
    dt = e[3].strip()
    if dt != "":
        dt = datetime.date(int(dt), 1, 1)
    else:
        dt = None
    d['data'] = dt
    
    c = e[4].capitalize().strip()
    if c == 'No' or c == 'Si':
        c = None
    d['colore'] = c
    
    v = e[5].strip()
    if v == "":
        v = None
    else:
        v = int(v)
    d['valore'] = v
    
    n = e[6].strip()
    if n != "":
        n = int(n)
    else:
        n = None
    d['numero_bollino'] = n
    d['scadenza'] = None
    d['note'] = None
    
    return d

	
def load_cliente(e):
    table_dict = {}

    if e[0].strip() != '':
        id = int(e[0], 10)
    else:
        id = None
    table_dict['codice_id'] = id

    table_dict['cognome'] = e[1].capitalize().strip()
    table_dict['nome'] = e[2].capitalize().strip()

    if e[3].strip() != '':
        cdf = e[3].upper().strip()
    else:
        cdf = ""
    table_dict['codice_fiscale'] = cdf

    table_dict['via'] = e[4].capitalize().strip()
    table_dict['citta'] = e[5].capitalize().strip()

    if e[6].strip() != '':
        tel = e[6].replace(' ', '')
    else:
        tel = None
    table_dict['numero_telefono'] = tel

    table_dict['marca_caldaia'] = e[7].strip().upper()
    table_dict['modello_caldaia'] = e[8].strip().upper()
    table_dict['tipo'] = e[9].strip().upper()
    table_dict['combustibile'] = e[10].strip().capitalize()

    table_dict['data_installazione'] = data_fmt(e[11])
    table_dict['data_contratto'] = data_fmt(e[12])	

    return table_dict


def dump(l, key = None):
    if key is not None:
        print l[key]
    else:
        print l
        for i in l.keys():
            print l[i],

        print

def dump_all(l, key = None):
    for i in l:
        dump(i, key)

def load_all():
    cli = load_csv("main/elenco2010.csv", load_cliente)
    bol = load_csv("main/bollino.csv", load_bollino)
    return cli, bol 

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print sys.argv[0], " <csv file name>"
        exit (1)
    
    all = load_csv(sys.argv[1], load_bollino)
    print all
    
    print "Records: ", len(all)