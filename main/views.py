from django import http
from django.shortcuts import render

from main import models
from main import myforms
from main import clienti



def scheda_cliente(req):
    id = req.GET.get('id','')
    search_str = req.GET.get('s', '')
    if id == "":
        return render(req, 'errors.sub',
        {'error': "Id sbagliato." })

    cli = clienti.select_record(models.Cliente.objects, int(id))
    bol = clienti.select_bollini(cli)
    intr = clienti.select_interventi(cli)    
    bollini_history = len(bol)
    interventi_history = len(intr)

    if bollini_history >= 1:
        bol = bol[0]
    if interventi_history >= 1:
        intr = intr[0]
    
    return render(req, 'anagrafe_scheda.sub',
    {'error': 0,
     'search_string':search_str,
     'cliente': cli,
     'bollino': bol,
     'intervento': intr,
     'history_bollini_len': bollini_history,
     'history_interventi_len': interventi_history,
     'empty_cell':"-"
    })

def manage_clienteRecord(req):
    form = models.ClienteForm()
    if req.method == 'POST':
        form = models.ClienteForm(req.POST)
        print form
        if form.is_valid():
            return render(req, 'anagrafe_new.sub', {'cliente': form })
    
    if req.method == 'GET':
        id = req.GET.get('id','')
        if id != "":
            select = clienti.select_record(models.Cliente.objects, int(id))
            form = models.ClienteForm(instance=select)

    return render(req, 'anagrafe_new.sub', {'cliente': form })

def anagrafe(req):
    form = myforms.FullTextSearchForm()
    search_str = ""
    
    if req.method == 'POST':
        form = myforms.FullTextSearchForm(req.POST)
        if form.is_valid():
            search_str = form.cleaned_data['search_string']
            data_to_render = clienti.search_fullText(models.Cliente.objects, search_str)
        else:
            """stringa vuota faccio vedere tutto"""
            form = myforms.FullTextSearchForm()
            data_to_render = clienti.clienti_displayAll(models.Cliente.objects)
            search_str = ""
                        
        return render(req, 'anagrafe.sub',
            {'clienti': data_to_render,
             'search_string': search_str,
             'display_data':1,
             'empty_cell':"-",
             'form': form })

    return render(req, 'anagrafe.sub', {'display_data':0, 'form': form })


