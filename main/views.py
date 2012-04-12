from django import http
from main import models
from main import clienti
from django.shortcuts import render_to_response


def test(req):
    filtro = req.GET.get('q', '')
    return render_to_response('test.html', {'clienti': clienti.filter_records(models.Cliente.objects, "cognome", filtro)})


