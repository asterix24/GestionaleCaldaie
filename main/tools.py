#!/usr/bin/env python

import clienti
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
            table_dict = handler(e)
        except ValueError, m:
            print "ValueError (%s)" % m , e
            exit (0)

        all.append(table_dict)

    return all

def load_intervento(e):
    ref = {}
    d = {}
    ref['id'] = int(e[0].strip())
    d['data'] = data_fmt(e[1])
    d['tipo'] = e[2].strip()
    d['numero_rapporto'] = int(e[3].strip())
    d['scadenza'] = int(e[4].strip())
    d['data_scadenza'] = data_fmt(e[5])
    d['note'] = e[6]
    
    return [ref, d]

	
def load_cliente(e):

    table_dict = {}

    if e[0].strip() != '':
        id = int(e[0], 10)
    else:
        id = None
    table_dict['codice_id'] = id
    
    table_dict['codice_impianto'] = None

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
        cell = e[6].replace(' ', '')
    else:
        cell = None
    
    if e[7].strip() != '':
        tel = e[7].replace(' ', '')
        
        if tel[0] != '0':
            cell = tel
            tel = None
    else:
        tel = None
    
    table_dict['numero_telefono'] = cell    
    table_dict['numero_cellulare'] = tel
    
    table_dict['mail'] = None
    
    table_dict['marca_caldaia'] = e[8].strip().upper()
    table_dict['tipo'] = e[9].strip().upper()
    table_dict['modello_caldaia'] = e[10].strip().upper()

    table_dict['combustibile'] = e[11].strip().capitalize()

    table_dict['data_installazione'] = data_fmt(e[12])
    table_dict['data_contratto'] = data_fmt(e[13])	

    table_bollino = {}
    p = 0
    if e[14].lower() == 'si':
        p = 1
    table_bollino['presente'] = p
    
    dt = e[15].strip()
    if dt != "":
        dt = datetime.date(int(dt), 1, 1)
    else:
        dt = None
    table_bollino['data'] = dt
    
    c = e[16].capitalize().strip()
    if c == 'No' or c == 'Si':
        c = None
    table_bollino['colore'] = c
    
    v = e[17].strip()
    if v == "":
        v = None
    else:
        v = int(v)
    table_bollino['valore'] = v
    
    n = e[18].strip()
    if n != "":
        n = int(n)
    else:
        n = None
    table_bollino['numero_bollino'] = n
    table_bollino['scadenza'] = None
    table_bollino['note'] = None

    return [table_dict, table_bollino]


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
    int = load_csv("main/interventi.csv", load_intervento)
    
    clienti.insert_clientiBollini(cli)
    clienti.insert_interventi(int)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print sys.argv[0], " <csv file name>"
        exit (1)
    
    all = load_csv(sys.argv[1], load_cliente)
    print all
    
    print "Records: ", len(all)