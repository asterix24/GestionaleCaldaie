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

def _display_error(request, msg):
    return render(request, 'messages.sub',
            { 'msg_hdr':'Error!',
              'msg_body': msg })

def _display_ok(request, msg):
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

    dr = data_render.DataRender(data_to_render)

    if detail_type is None:
        if len(data_to_render) >= 1 and data_to_render[0]['cliente_impianto_id'] != None:
            dr.selectColums(data_render.SCHEDA_ANAGRAFE_IMPIANTI)
            dr.urlBar('impianto', ['edit','remove'])
            dr.urlBarAdd(record_id, sub_record_id)
            data += dr.toTable()
        else:
            # Aggiundi modificatori alle tabelle con il link giusto per aggiungere un impianto.
            data += "Aggiungi Impianto al cliente.."


    elif detail_type == "impianto":
        data_to_render = database_manager.search_impiantoId(sub_record_id)
        data += data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE_IMPIANTI, "Dettaglio Impianto")

        dr.selectColums(data_render.SCHEDA_ANAGRAFE_VERIFICHE)
        dr.urlBar('verifiche', ['edit','remove'])
        dr.urlBarAdd(record_id, sub_record_id)
        data += dr.toTable()

    elif detail_type == "verifiche":
        data_to_render = database_manager.search_verificheId(sub_record_id)
        data += data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE_VERIFICHE, "Dettaglio Verifiche e Manutenzioni")

    elif detail_type == "intervento":
        data_to_render = database_manager.search_interventoId(sub_record_id)
        data += data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE_INTERVENTI, "Dettaglio Intervento")

    else:
        data = None

    return data

def add_record(request, record_id = None, detail_type = None, sub_record_id = None):
    if request.method == 'GET':
        if record_id is None:
            form = models.ClienteForm()
            header_msg = "Aggiungi Nuovo Cliente"
            post_url = "add/"
            return_url = ""

        else:
            if detail_type == 'impianto':
                form = models.ImpiantoForm(initial={'cliente_impianto': models.Cliente.objects.get(pk=record_id)})
                header_msg = "Aggiungi Nuovo Impianto"
                post_url = "%s/impianto/add/" % record_id
                return_url = "%s/" % record_id

            if detail_type == 'verifiche':
                form = models.VerificheForm(initial={'verifiche_impianto': models.Impianto.objects.get(pk=record_id)})
                header_msg = "Aggiungi Nuova Verifica e Manutenzione"
                post_url = "%s/impianto/%s/verifiche/add/" % (record_id, sub_record_id)
                return_url = "%s/impianto/%s/" % (record_id, sub_record_id)

            if detail_type == 'intervento':
                form = models.InterventoForm(initial={'intervento_impianto': models.Impianto.objects.get(pk=record_id)})
                header_msg = "Aggiungi Nuovo Intervento"
                post_url = "%s/impianto/%s/intervento/add/" % (record_id, sub_record_id)
                return_url = "%s/impianto/%s/" % (record_id, sub_record_id)

        return render(request, 'anagrafe_add.sub', {'header_msg': header_msg, 'data': form,
            'post_url':post_url, 'return_url':return_url})

    if request.method == 'POST':
        form = models.ClienteForm(request.POST)
        if form.is_valid():
            instance = form.save()
            data = view_record(instance.id)
            if data is None:
                return _display_error(request, "Qualcosa e' andato storto..")

        return render(request, 'anagrafe_scheda.sub', {'data': data })
    else:
        return render(request, 'anagrafe_add.sub', {'action': 'Nuovo', 'cliente': form})

    return _display_error(request, "Qualcosa e' andato storto..")

def delete_record(request, record_id):
    try:
            if request.method == 'GET':
                    data = view_record(record_id)
                    return render(request, 'anagrafe_manager.sub',
                            {'data': data ,
                             'top_message': '<h1>Attenzione! stai per cancellare tutti i dati del seguente cliente.</h1>',
                             'record_id': record_id})

            if request.method == 'POST':
                    #data = view_record(record_id)
                    cli = database_manager.select_record(models.Cliente.objects, record_id)
                    nome = cli.nome
                    cognome = cli.cognome
                    cli.delete()
                    s = "Cliente: %s %s Rimosso correttamente." % (nome, cognome)
                    return _display_ok(request, s)

    except ObjectDoesNotExist, m:
            return _display_error(request, "Qualcosa e' andato storto..(%s)" % m)

    return _display_error(request, "Qualcosa e' andato storto..")

def edit_record(request, record_id):
    if request.method == 'GET':
        if record_id != "":
            select = database_manager.select_record(models.Cliente.objects, record_id)
            form = models.ClienteForm(instance=select)
            return render(request, 'anagrafe_add.sub', {'action': 'Modifica',
                                                    'record_id': record_id,
                                                    'cliente': form})
        else:
            return _display_error(request, "Id non trovato.")

    # We manage a post request when we want to save the data.
    if request.method == 'POST':
        #If we found a id take the record to edit it.
        if record_id != "":
            select = database_manager.select_record(models.Cliente.objects, record_id)
            form = models.ClienteForm(request.POST, instance=select)

        if form.is_valid():
            form.save()
            return _display_scheda(request, record_id)
        else:
            return render(request, 'anagrafe_add.sub', {'action': 'Modifica',
                                                        'record_id': record_id,
                                                        'cliente': form})
    else:
        return _display_error(request, "Id non trovato.")


def detail_record(request, record_id, detail_type = None, sub_record_id = None):

    data = view_record(record_id, detail_type, sub_record_id)

    if data is None:
        _display_error(request, "Qualcosa e' andato storto!")

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
            dr = data_render.DataRender(data_to_render)
            dr.selectColums(data_render.ANAGRAFE_COLUM)
            dr.urlBar('cliente', ['edit', 'remove', 'add'])
            dr.msgItemsEmpty("<br><h3>La ricerca non ha prodotto risultati.</h3>")
            data += dr.toTable()

    return render(request, 'anagrafe.sub', {'data': data,'form': form })


from main import tools

def populatedb(request):
    data = tools.insert_csv_files(cli_on=False)
    return _display_ok(request, "DB aggiornato con sucesso\n" + data)


