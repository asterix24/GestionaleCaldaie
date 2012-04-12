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
    return node

def insert_intervento(cli, interv):
    node = Intervento(cliente=cli, **interv)
    dump(interv)
    node.save()
    return node
    
def insert_bollino(cli, bl):
    node = Bollino(cliente=cli, **bl)
    dump(bl)
    node.save()
    return node        
        
def select_bollini(cli):
    return cli.bollino_set.values()

def select_interventi(cli):
    return cli.intervento_set.values()
        
def insert_clientiBollini(all):
    for i in all:
        cli = insert_cliente(i[0])
        insert_bollino(cli, i[1])

def insert_interventi(all):
    for i in all:
        cli = select_record(Cliente.objects, i[0]['id'])
        insert_intervento(cli, i[1])

