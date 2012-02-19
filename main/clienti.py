#!/usr/bin/env python

def open_csv(file_name):
    import csv

    table = csv.reader(open(file_name, 'rb'), delimiter=',', quotechar='\"')

    for e in table:
        print e[0]




if __name__ == "__main__":
    import sys
    import csv

    if len(sys.argv) < 2:
        print sys.argv[0], " <csv file name>"

    table = csv.reader(open(sys.argv[1], 'rb'), delimiter=',', quotechar='\"')
    all = []

    for e in table:
        #print e
        table_dict = {}
        try:
            #print e[0], type(e[0])
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

            table_dict['data_installazione'] = e[11].strip()
            table_dict['data_contratto'] = e[12].strip()

        except ValueError:
            print "errore", e
            exit (0)



        all.append(table_dict)

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
