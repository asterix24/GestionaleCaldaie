from django import http
from main import models
from main import clienti

from django.shortcuts import render_to_response
from django.forms.models import modelformset_factory
from django.http import HttpResponse

def test(req):
    filtro = req.GET.get('q', '')
    print req.GET.keys()
    print req.GET.values()
    return render_to_response('test.html',
        {'clienti': clienti.filter_records(models.Cliente.objects, "cognome", filtro)}
        )
        
def edit(req):
    filtro = req.GET.get('q', '')
    select = clienti.filter_records(models.Cliente.objects, "cognome", filtro)
    html = modelformset_factory(models.Cliente)
    return HttpResponse(html(queryset=select))
        
def home(req):
    filtro = req.GET.get('q', '')
    select = clienti.filter_records(models.Cliente.objects, "cognome", filtro)
    html = modelformset_factory(select)
    return HttpResponse(html())

