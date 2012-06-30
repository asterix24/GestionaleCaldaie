#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import http
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from main import models
from main import myforms
from main import tools
from main import data_render
from main import database_manager

def home(request):
    return render(request, 'home.sub', {})

def _diplay_error(request, msg):
    return render(request, 'messages.sub',
        { 'msg_hdr':'Error!',
          'msg_body': msg })

def _diplay_ok(request, msg):
    return render(request, 'messages.sub',
        { 'msg_hdr':'Ok!',
          'msg_body': msg})


def _detail_select(request, record_id, detail_type=None, msg=''):
    cliente = database_manager.select_record(models.Cliente.objects, record_id)

    if detail_type is None:
        return _diplay_error(request, "Detail non sensato..")

    if detail_type == "interventi":
        data_to_render = database_manager.select_interventi(cliente)
    else:
        data_to_render = database_manager.select_bollini(cliente)

    return render(request, 'anagrafe_scheda_history.sub',{ 'top_msg':msg,
                                                   'cliente': cliente,
                                                   'detail_type':detail_type,
                                                   'data_to_render': data_to_render})

def _diplay_scheda(request, record_id, msg=''):
    cliente = database_manager.select_record(models.Cliente.objects, record_id)
    bollini = database_manager.select_bollini(cliente)
    interventi = database_manager.select_interventi(cliente)

    bollini_history = len(bollini)
    if bollini_history >= 1:
        bollini = bollini[0]

    interventi_history = len(interventi)
    if interventi_history >= 1:
        interventi = interventi[0]

    return render(request, 'anagrafe_scheda.sub',
                    {'top_msg':msg,
                     'cliente': cliente,
                     'bollino': bollini,
                     'intervento': interventi,
                     'interventi_history': interventi_history,
                     'bollini_history': bollini_history,
                    })

def detail_record(request, record_id, detail_type = None):
    if record_id == "":
        _diplay_error(request, "Id non trovato.")

    if detail_type == "detail":
        return _diplay_scheda(request, record_id)
    else:
        return _detail_select(request, record_id, detail_type, "")

def edit_record(request, record_id):
    if request.method == 'GET':
        if record_id != "":
            select = database_manager.select_record(models.Cliente.objects, record_id)
            form = models.ClienteForm(instance=select)
            return render(request, 'anagrafe_new.sub', {'action': 'Modifica',
                                                        'record_id': record_id,
                                                        'cliente': form})
        else:
            return _diplay_error(request, "Id non trovato.")

    # We manage a post request when we want to save the data.
    if request.method == 'POST':
        #If we found a id take the record to edit it.
        if record_id != "":
            select = database_manager.select_record(models.Cliente.objects, record_id)
            form = models.ClienteForm(request.POST, instance=select)

            if form.is_valid():
                form.save()
                return _diplay_scheda(request, record_id)
            else:
                return render(request, 'anagrafe_new.sub', {'action': 'Modifica',
                                                        'record_id': record_id,
                                                        'cliente': form})
        else:
            return _diplay_error(request, "Id non trovato.")

def new_record(request):
    if request.method == 'GET':
        form = models.ClienteForm()
        return render(request, 'anagrafe_new.sub', {'action': 'Nuovo',
                                                'cliente': form})
    if request.method == 'POST':
        form = models.ClienteForm(request.POST)
        if form.is_valid():
            istance = form.save()
            s = "Cliente: %s %s aggiunto correttamente." % (request.POST.get('nome'), request.POST.get('cognome'))
            return _diplay_scheda(request, istance.id, s)
        else:
            return render(request, 'anagrafe_new.sub', {'action': 'Nuovo',
                                                    'cliente': form})

    return _diplay_error(request, "Qualcosa e' andato storto..")

def delete_record(request, record_id):
    try:
        if request.method == 'GET':
            return render(request, 'anagrafe_delete.sub', {'record_id':record_id,
                                                           'cliente': database_manager.select_record(models.Cliente.objects, record_id)})

        if request.method == 'POST':
            cli = database_manager.select_record(models.Cliente.objects, record_id)
            nome = cli.nome
            cognome = cli.cognome
            cli.delete()
            s = "Cliente: %s %s Rimosso correttamente." % (nome, cognome)
            return _diplay_ok(request, s)

    except ObjectDoesNotExist, m:
        return _diplay_error(request, "Qualcosa e' andato storto..(%s)" % m)

    return _diplay_error(request, "Qualcosa e' andato storto..")

def _model_form(record_type):
    if record_type is None:
        return None

    if record_type == "intervento":
        model_form = models.InterventoForm
    else:
        model_form = models.BollinoForm

    return model_form

def _model_ctx(record_type, record_type_id):
    if record_type is None:
        return None

    if record_type == "intervento":
        model_ctx = database_manager.select_interventi(models.Intervento.objects, record_type_id)
    else:
        model_ctx = database_manager.select_bollini(models.Bollino.objects, record_type_id)

    return model_ctx

def new_typeRecord(request, record_id = None, record_type = None):

    model_form = _model_form(record_type)
    if model_form is None:
        return _diplay_error(request, "Qualcosa e' andato storto..")

    if request.method == 'GET':
        if record_id is None:
            form = model_form()
        else:
            form = model_form(initial={'cliente': database_manager.select_record(models.Cliente.objects, record_id)})

        return render(request, 'record_type_mgr.sub', {'action': 'Nuovo',
                                                      'form': form,
                                                      'record_id': record_id,
                                                      'record_type': record_type })

    if request.method == 'POST':
        form = model_form(request.POST)

        if form.is_valid():
            record_id = form.cleaned_data['cliente'].id
            form.save()
            if record_type == "intervento":
                s = "L\'intervento \"%s\" del %s e' stato aggiunto correttamente." % (models.interventi_choicesExteded(form.cleaned_data['tipo']), form.cleaned_data['data'].strftime("%d/%m/%y"))
            else:
                s = "Il Bollino e' stato aggiunto correttamente."
            return _diplay_scheda(request, record_id, s)

        else:
            return render(request, 'record_type_mgr.sub', {'action': 'Nuovo',
                                                          'form': form,
                                                          'record_id': record_id,
                                                          'record_type': record_type })

    return _diplay_error(request, "Qualcosa e' andato storto..")

def edit_typeRecord(request, record_id = None, record_type = None, record_type_id = None):
    model_form = _model_form(record_type)
    if model_form is None:
        return _diplay_error(request, "Qualcosa e' andato storto..")

    if request.method == 'GET':
        if record_type_id is not None:
            form = model_form(instance=_model_ctx(record_type, record_type_id))
        else:
            form = model_form()

        return render(request, 'record_type_mgr.sub', {'action': 'Modifica',
                                                       'form': form,
                                                        'record_id': record_id,
                                                        'record_type': record_type,
                                                        'record_type_id': record_type_id})

    if request.method == 'POST':
        if record_type_id is not None:
            form = model_form(request.POST, instance=_model_ctx(record_type, record_type_id))
        else:
            form = model_form(request.POST)

        if form.is_valid():
            record_id = form.cleaned_data['cliente'].id
            form.save()

            if record_type == "intervento":
                s = "L\'Intervento del %s e' stato modificato correttamente." % form.cleaned_data['data'].strftime("%d/%m/%y")
            else:
                s = "Il Bollino e\' stato modificato correttamente."

            return _diplay_scheda(request, record_id, s)
        else:
            return render(request, 'record_type_mgr.sub', {'action': 'Modifica',
                                                           'form': form,
                                                           'record_id': record_id,
                                                           'record_type': record_type,
                                                           'record_type_id': record_type_id})

    return _diplay_error(request, "Qualcosa e' andato storto..")

def delete_typeRecord(request, record_id = None, record_type = None, record_type_id = None):
    if record_type is None:
        return _diplay_error(request, "Qualcosa e' andato storto..")

    try:
        if request.method == 'GET':

            return render(request, 'record_type_delete.sub', {'action': 'Cancella',
                                                           record_type: _model_ctx(record_type, record_type_id),
                                                           'record_id': record_id,
                                                           'record_type': record_type,
                                                           'record_type_id': record_type_id})

        if request.method == 'POST':
            record = _model_ctx(record_type, record_type_id)

            if record_type == "intervento":
                try:
                    data = record.data.strftime("%d/%m/%y")
                except ValueError:
                    data = ""
                tipo = models.interventi_choicesExteded(record.tipo)
                s = "Intervento \"%s\" del %s, rimosso correttamente." % (tipo, data)
            else:
                s = "Il Bollino e\' stato rimosso correttamente."

            record.delete()
            return _diplay_scheda(request, record_id, s)

    except ObjectDoesNotExist, m:
        return _diplay_error(request, "Qualcosa e' andato storto..(%s)" % m)

    return _diplay_error(request, "Qualcosa e' andato storto..")


ANAGRAFE_COLUM=[
	'cognome',
	'nome',
	'codice_fiscale',
	'via',
	'citta',
	]

def test(request):
    t = database_manager.table_doDict(models.Cliente.objects.all())
    table = data_render.render_toTable(t, show_colum=ANAGRAFE_COLUM)
    return render(request, 'test', {'data':table})

def anagrafe(request):
    form = myforms.FullTextSearchForm()
    data = ""

    if request.method == 'GET' and request.GET != {}:
        form = myforms.FullTextSearchForm(request.GET)
        if form.is_valid():
            data_to_render = database_manager.search_fullText(models.Cliente.objects, form.cleaned_data['s'])
        else:
            """stringa vuota faccio vedere tutto"""
            form = myforms.FullTextSearchForm()
            data_to_render = database_manager.database_manager_displayAll(models.Cliente.objects)

        if data_to_render != "":
            data = render_toTable(data_to_render)
        else:
            data = "<tr><h2>La ricerca non ha prodotto risultati</h2></tr>"

    return render(request, 'anagrafe.sub', {'data': data,'form': form })
