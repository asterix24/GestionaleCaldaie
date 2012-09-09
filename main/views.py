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

def test(request):
    return render(request, 'test', {'data':""})

def view_record(record_id, detail_type = None, sub_record_id = None):

    if record_id == "":
            return None

    data_to_render = database_manager.search_clienteId(record_id)
    data = data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE, "Dettaglio Cliente")

    if detail_type is None:
        if len(data_to_render) >= 1 and data_to_render[0]['cliente_impianto_id'] != None:
            bar = data_render.add_editBarUrl(record_id, "impianto", sub_record_id)
            data += data_render.render_toTable(data_to_render, show_colum=data_render.SCHEDA_ANAGRAFE_IMPIANTI, decorator=bar)
        else:
            # Aggiundi modificatori alle tabelle con il link giusto per aggiungere un impianto.
            data += "Aggiungi Impianto al cliente.."


    elif detail_type == "impianto":
        data_to_render = database_manager.search_impiantoId(sub_record_id)
        bar = data_render.add_editBarUrl(record_id, "verifiche", sub_record_id)
        data += data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE_IMPIANTI, "Dettaglio Impianto")
        data += data_render.render_toTable(data_to_render, show_colum=data_render.SCHEDA_ANAGRAFE_VERIFICHE, decorator=bar)

    elif detail_type == "verifiche":
        data_to_render = database_manager.search_verificheId(sub_record_id)
        data += data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE_VERIFICHE, "Dettaglio Verifiche e Manutenzioni")

    elif detail_type == "intervento":
        data_to_render = database_manager.search_interventoId(sub_record_id)
        data += data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE_INTERVENTI, "Dettaglio Intervento")

    else:
        data = None

    return data

def new_record(request):
    if request.method == 'GET':
            form = models.ClienteForm()
            return render(request, 'anagrafe_new.sub', {'action': 'Nuovo', 'cliente': form})
    if request.method == 'POST':
            form = models.ClienteForm(request.POST)
            if form.is_valid():
                instance = form.save()
                data = view_record(instance.id)
                if data is None:
                    return _diplay_error(request, "Qualcosa e' andato storto..")

                return render(request, 'anagrafe_scheda.sub', {'data': data })
            else:
                return render(request, 'anagrafe_new.sub', {'action': 'Nuovo', 'cliente': form})

    return _diplay_error(request, "Qualcosa e' andato storto..")

def delete_record(request, record_id):
    try:
            if request.method == 'GET':
                    data = view_record(record_id)
                    return render(request, 'anagrafe_manager.sub',
                            {'data': data ,
                             'top_message': '<h1>Attenzione! stai per cancellare il Cliente selezionato e tutto la sua storia.</h1>',
                             'record_id': record_id})

            if request.method == 'POST':
                    #data = view_record(record_id)
                    cli = database_manager.select_record(models.Cliente.objects, record_id)
                    nome = cli.nome
                    cognome = cli.cognome
                    cli.delete()
                    s = "Cliente: %s %s Rimosso correttamente." % (nome, cognome)
                    return _diplay_ok(request, s)

    except ObjectDoesNotExist, m:
            return _diplay_error(request, "Qualcosa e' andato storto..(%s)" % m)

    return _diplay_error(request, "Qualcosa e' andato storto..")

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


def detail_record(request, record_id, detail_type = None, sub_record_id = None):

    data = view_record(record_id, detail_type, sub_record_id)

    if data is None:
        _diplay_error(request, "Qualcosa e' andato storto!")

    return render(request, 'anagrafe_scheda.sub', {'data': data , 'record_id': record_id})

def anagrafe(request):
    form = myforms.FullTextSearchForm()
    search_string = ""
    data = ""

    if request.method == 'GET' and request.GET != {}:
            form = myforms.FullTextSearchForm(request.GET)
            if form.is_valid():
                    search_string = form.cleaned_data['s']

            data_to_render = database_manager.search_fullText(search_string)
            data = data_render.render_toTable(data_to_render, show_colum=data_render.ANAGRAFE_COLUM)

    return render(request, 'anagrafe.sub', {'data': data,'form': form })
