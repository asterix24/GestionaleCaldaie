from django import http
from main import models
from main import myforms
from main import clienti

from django.shortcuts import render_to_response
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render

def test(req):
    return render(req, 'template.html')
    """
    return render_to_response('template.html',
        RequestContext(req, {})
        )
    return render_to_response('test.html',
        {'clienti': clienti.filter_records(models.Cliente.objects, "cognome", filtro)}
        )
    """
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


def edit(req):
    id = req.GET.get('id','')
    if id == "":
        return render(req, 'errors.sub',
        {'error': "Id sbagliato." })

    select = clienti.select_record(models.Cliente.objects, int(id))
    html = modelformset_factory(models.Cliente)
    return HttpResponse(html(queryset=select))

def new_record(req):
    clienti_formset = modelformset_factory(models.Cliente)
    return render(req, 'anagrafe_new.sub',
                    {'formset': clienti_formset(queryset=models.Cliente.objects.get(pk=1)) })


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

    if req.GET == {}:
        return render(req, 'anagrafe.sub',
           {'display_data':0,
           'form': form })
    else:
        return render(req, 'anagrafe.sub',
            {'clienti': clienti.filter_records(models.Cliente.objects, req.GET.keys()[0], req.GET.values()[0]),
            'display_data':1,
            'empty_cell':"-",
            'form': form })


