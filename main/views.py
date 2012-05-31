from django import http
from django.shortcuts import render

from main import models
from main import myforms
from main import clienti

def test(request, record_id):
    return _diplay_Scheda(request, record_id)

def _diplay_error(request):
    return render(request, 'errors.sub',
        {'error': "Id sbagliato." })
    
def _diplay_Scheda(request, record_id=''):
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
     'cliente': cli,
     'bollino': bol,
     'intervento': intr,
     'history_bollini_len': bollini_history,
     'history_interventi_len': interventi_history,
     'empty_cell':"-"
    })

def detail_record(request, record_id):
    if record_id == "":
        _diplay_error(request)

    return _diplay_Scheda(request, record_id)

def edit_record(request, record_id):
    if request.method == 'GET':
        if record_id != "":
            select = clienti.select_record(models.Cliente.objects, record_id)
            form = models.ClienteForm(instance=select)
            return render(request, 'anagrafe_new.sub', {'action': 'Modifica',
                                                        'record_id': record_id,
                                                        'cliente': form})
        else:
            return _diplay_error(request)
    
    # We manage a post request when we want to save the data.        
    if request.method == 'POST':
        #If we found a id take the record to edit it.
        if record_id != "":
            select = clienti.select_record(models.Cliente.objects, record_id)
            form = models.ClienteForm(request.POST, instance=select)
            
            if form.is_valid():
                form.save()
                return _diplay_Scheda(request, record_id)
        else:
            return _diplay_error(request)

def new_record(request):
    return _diplay_error(request)

def anagrafe(req):
    form = myforms.FullTextSearchForm()
    search_str = ""
    
    if req.method == 'GET' and req.GET != {}:
        form = myforms.FullTextSearchForm(req.GET)
        if form.is_valid():
            search_str = form.cleaned_data['s']
            data_to_render = clienti.search_fullText(models.Cliente.objects, search_str)
        else:
            """stringa vuota faccio vedere tutto"""
            form = myforms.FullTextSearchForm()
            data_to_render = clienti.clienti_displayAll(models.Cliente.objects)
            search_str = ""
                        
        return render(req, 'anagrafe.sub',
            {'clienti': data_to_render,
             'display_data':1,
             'display_search_bot':1,
             'empty_cell':"-",
             'form': form })

    return render(req, 'anagrafe.sub', {'display_data':0,
                                        'display_search_bot':0,
                                        'form': form })


