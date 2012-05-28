from django import http
from django.shortcuts import render

from main import models
from main import myforms
from main import clienti

def _diplay_Scheda(request, record_id='', search_str=''):    
    cli = clienti.select_record(models.Cliente.objects, int(record_id))
    bol = clienti.select_bollini(cli)
    intr = clienti.select_interventi(cli)    
    bollini_history = len(bol)
    interventi_history = len(intr)

    if bollini_history >= 1:
        bol = bol[0]
    if interventi_history >= 1:
        intr = intr[0]
    
    return render(request, 'anagrafe_scheda.sub',
    {'error': 0,
     'search_string':search_str,
     'cliente': cli,
     'bollino': bol,
     'intervento': intr,
     'history_bollini_len': bollini_history,
     'history_interventi_len': interventi_history,
     'empty_cell':"-"
    })


def scheda_cliente(request):
    record_id = request.GET.get('id','')
    search_str = request.GET.get('s', '')
    
    if record_id == "":
        return render(request, 'errors.sub',
        {'error': "Id sbagliato." })
    
    return _diplay_Scheda(request, record_id, search_str)

def edit_record(req):
    if req.method == 'GET':
        record_id = req.GET.get('id','')
        #If we found a id take the record to edit it.
        if record_id != "":
            select = clienti.select_record(models.Cliente.objects, int(record_id))
            form = models.ClienteForm(instance=select)
            return render(req, 'anagrafe_new.sub', {'action': 'Modifica',
                                                    'cliente': form,
                                                    'record_id':record_id})
        else:
            return render(req, 'errors.sub', {'error': "Id sbagliato." })
            
    if req.method == 'POST':
        record_id = req.POST.get('id','')
        search_str = req.POST.get('s', '')
        #If we found a id take the record to edit it.
        if record_id != "":
            select = clienti.select_record(models.Cliente.objects, int(record_id))
            form = models.ClienteForm(req.POST, instance=select)
            if form.is_valid():
                form.save()
                return _diplay_Scheda(req, record_id, search_str)
        else:
            return render(req, 'errors.sub', {'error': "Id sbagliato." })

def new_record(req):
    pass

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


