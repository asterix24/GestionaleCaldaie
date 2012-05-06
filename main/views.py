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
    print req.GET.get('id','');
    return render(req, 'base.html')

def edit(req):
    filtro = req.GET.get('q', '')
    select = clienti.filter_records(models.Cliente.objects, "cognome", filtro)
    html = modelformset_factory(models.Cliente)
    return HttpResponse(html(queryset=select))


def anagrafe(req):
    form = myforms.FullTextSearchForm()
    if req.method == 'POST':
        if req.POST.get('advanced_search','') == 0:
            form = myforms.FullTextSearchForm(req.POST)
            if form.is_valid():
                print form.cleaned_data['search_string']
            else:
                print "non valido"
        else:
            print "Ricerca avanzata"
            form = myforms.SearchCliente()

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

def home(req):
    filtro = req.GET.get('q', '')
    select = clienti.filter_records(models.Cliente.objects, "cognome", filtro)
    html = modelformset_factory(select)
    return HttpResponse(html())

