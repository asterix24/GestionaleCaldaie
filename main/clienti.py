#!/usr/bin/env python

def insertCliente(clienti):
    for l in clienti:
        node = Cliente(codice_id = l['codice_id'],
                nome = l['nome'],
                cognome = l['cognome'],
                codice_fiscale = l['codice_fiscale'],
                via = l['via'],
                citta = l['citta'],
                numero_telefonico = l['numero_telefono'],
                marca_caldaia = l['marca_caldaia'],
                modello_caldaia = l['modello_caldaia'],
                tipo = l['tipo'],
                combustibile = l['combustibile'],
                data_installazione = l['data_installazione'],
                data_contratto = l['data_contratto'])

        node.save()


def load_csv(file_name):
    import csv
    import datetime
    table = csv.reader(open(file_name, 'rb'), delimiter=',', quotechar='\"')
    all = []

    for e in table:
        table_dict = {}
        try:
            if e[0].strip() != '':
                id = int(e[0], 10)
            else:
                id = 0

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
                tel = 0
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
                dinst = datetime.date

            table_dict['data_installazione'] = dinst

            if (e[12].strip() != ""):
                raw = e[12].replace(".", "/")
                d, m, y = raw.split("/")
                dcont = datetime.date(int(y), int(m), int(d))
            else:
                dcont = datetime.date
            table_dict['data_contratto'] = dcont

        except ValueError, m:
            print "errore (%s)" % m , e
            exit (0)


        all.append(table_dict)

    return all


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print sys.argv[0], " <csv file name>"

    all = load_csv(sys.argv[1])
    i = 0
    for l in all:
        i += 1
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

    print "Records: ", i
