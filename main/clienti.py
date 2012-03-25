#!/usr/bin/env python
import datetime
from tools import *
from models import Cliente
from models import Intervento
from models import Bollino


FILTER_MODE_START =    '__istartswith'
FILTER_MODE_EXACT =    '__iexact'
FILTER_MODE_CONTAIN =  '__icontains'
FILTER_SHORT_ASCEN =   0
FILTER_SHORT_DESCEND = 1

def filter_records(ctx, key, value, mode = FILTER_MODE_CONTAIN):
    print key, value, mode
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

def insert_cliente(r):
    node = Cliente(**r)

    dump(r)
    node.save()

def insert_clienti(clienti):
    for l in clienti:
        insert_cliente(l)

def insert_intervento(cli, data_int, tipo_int, note_int):
    node = Intervento(data=data_int, tipo=tipo_int, note=note, cliente=cli)
    dump({"data":data_int, "tipo":tipo_int, "note":note, "cliente":cli})
    node.save()
    
def insert_bollino(bl):
    a = filter_records(Cliente.objects, "cognome", bl['cognome'], FILTER_MODE_EXACT)
    aa = filter_records(a, "nome", bl['nome'],FILTER_MODE_EXACT)
    del(bl['nome'])
    del(bl['cognome'])

    for i in aa:
        print i.numero_bollino
        bl['cliente'] = i
        node = Bollino(**bl)
        dump(bl)
        node.save()
    