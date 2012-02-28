#!/usr/bin/env python
from models import Cliente
import datetime

FILTER_MODE_START =    '__istartswith'
FILTER_MODE_EXACT =    '__iexact'
FILTER_MODE_CONTAIN =  '__icontains'
FILTER_SHORT_ASCEN =   0
FILTER_SHORT_DESCEND = 1

def filter_records(ctx, key, value, mode = FILTER_MODE_CONTAIN):
    return ctx.filter(**{ key + mode : value })

def filter_dataInstallazione(ctx, start_y, start_m = None, start_d = None, stop_y = None, stop_m = None, stop_d = None):
    if stop_y is not None and stop_m is not None and stop_d is not None:
        return ctx.filter(data_installazione__range = (datetime.date(start_y, start_m, start_d),datetime.date(stop_y, stop_m, stop_d)))
    if start_m is not None:
        return ctx.filter(data_installazione__year = start_y).filter(data_installazione__month = start_m)
    else:
        return ctx.filter(data_installazione__year = start_y)


def filter_dataContratto(ctx, start_y, start_m = None, start_d = None, stop_y = None, stop_m = None, stop_d = None):
    if stop_y is not None and stop_m is not None and stop_d is not None:
        return ctx.filter(data_contratto__range = (datetime.date(start_y, start_m, start_d),datetime.date(stop_y, stop_m, stop_d)))
    if start_m is not None:
        return ctx.filter(data_contratto__year = start_y).filter(data_installazione__month = start_m)
    else:
        return ctx.filter(data_contratto__year = start_y)

def update_record(ctx, id, key_value):
    return ctx.filter(pk__exact = id).update(**key_value)

def select_record(ctx, id):
    return ctx.get(pk=id)

def delete_record(ctx, id):
    return ctx.objects.get(pk=id).delete()

def insert_record(r):
    node = Cliente(**r)

    dump(r)
    node.save()

def insert_records(clienti):
    for l in clienti:
        insert_record(l)


def load_csv_cliente(file_name):
    import csv
    table = csv.reader(open(file_name, 'rb'), delimiter=',', quotechar='\"')
    all = []

    for e in table:
        table_dict = {}
        try:
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

            if (e[11].strip() != ""):
                raw = e[11].replace(".", "/")
                d, m, y = raw.split("/")
                dinst = datetime.date(int(y), int(m), int(d))
            else:
                dinst = None

            table_dict['data_installazione'] = dinst

            if (e[12].strip() != ""):
                raw = e[12].replace(".", "/")
                d, m, y = raw.split("/")
                dcont = datetime.date(int(y), int(m), int(d))
            else:
                dcont = None

            table_dict['data_contratto'] = dcont

        except ValueError, m:
            print "errore (%s)" % m , e
            exit (0)


        all.append(table_dict)

    return all

def dump(l, key = None):
    if key is not None:
        print l[key]
    else:
        print l['codice_id'],
        print l['nome'],
        print l['cognome'],
        print l['codice_fiscale'],
        print l['via'],
        print l['citta'],
        print l['numero_telefono'],
        print l['marca_caldaia'],
        print l['modello_caldaia'],
        print l['tipo'],
        print l['combustibile'],
        print l['data_installazione'],
        print l['data_contratto']

def dump_all(l, key = None):
    for i in l:
        dump(i, key)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print sys.argv[0], " <csv file name>"

    all = load_csv(sys.argv[1])
    i = 0
    for l in all:
        i += 1
        dump(l)

    print "Records: ", i
