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

def view_record(cliente_id, detail_type=None, impianto_id=None, sub_impianto_id=None):

    if cliente_id == "":
            return None

    data_to_render = database_manager.search_clienteId(cliente_id)
    data = data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE, "Dettaglio Cliente")

    dr = data_render.DataRender(data_to_render)

    if detail_type is None:
        if len(data_to_render) >= 1 and data_to_render[0]['cliente_impianto_id'] != None:
            dr.selectColums(data_render.SCHEDA_ANAGRAFE_IMPIANTI)
            dr.urlBar('impianto', ['edit','remove'])
            dr.urlBarAdd(cliente_id, impianto_id)
            data += dr.toTable()
        else:
            # Aggiundi modificatori alle tabelle con il link giusto per aggiungere un impianto.
            data += data_render.URL_DETAIL_ADD % ((cliente_id, "impianto") +
                             ('add', 'plus.jpg', 'aggiungi..', 'aggiungi..', '16', '16'))
            data += " Aggingi Impianto.."

    elif detail_type == "impianto":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        data += data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE_IMPIANTI, "Dettaglio Impianto")

        if data_to_render[0]['verifiche_id'] != None:
            dr.selectColums(data_render.SCHEDA_ANAGRAFE_VERIFICHE)
            dr.urlBar('verifiche', ['edit','remove'])
            dr.urlBarAdd(cliente_id, impianto_id)
            data += dr.toTable()
        else:
            # Aggiundi modificatori alle tabelle con il link giusto per aggiungere un impianto.
            data += data_render.URL_VERIFICHE_ADD % ((cliente_id, impianto_id, "verifiche") +
                             ('add', 'plus.jpg', 'aggiungi..', 'aggiungi..', '16', '16'))
            data += " Aggingi Verifiche.."

    elif detail_type == "verifiche":
        data_to_render = database_manager.search_verificheId(impianto_id)
        data += data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE_VERIFICHE, "Dettaglio Verifiche e Manutenzioni")

    elif detail_type == "intervento":
        data_to_render = database_manager.search_interventoId(impianto_id)
        data += data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE_INTERVENTI, "Dettaglio Intervento")

    else:
        data = None

    return data

def add_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    if cliente_id is None:
        header_msg = "Aggiungi Nuovo Cliente"
        post_url = "add/"
        return_url = ""

    else:
        if detail_type == 'impianto':
            header_msg = "Aggiungi Nuovo Impianto"
            post_url = "%s/impianto/add/" % cliente_id
            return_url = "%s/" % cliente_id

        if detail_type == 'verifiche':
            header_msg = "Aggiungi Nuova Verifica e Manutenzione"
            post_url = "%s/impianto/%s/verifiche/add/" % (cliente_id, impianto_id)
            return_url = "%s/impianto/%s/" % (cliente_id, impianto_id)

        if detail_type == 'intervento':
            header_msg = "Aggiungi Nuovo Intervento"
            post_url = "%s/impianto/%s/intervento/add/" % (cliente_id, impianto_id)
            return_url = "%s/impianto/%s/" % (cliente_id, impianto_id)

        if detail_type is None:
            return _display_error(request, "Qualcosa e' andato storto..")

    if request.method == 'GET':
        if cliente_id is None:
            form = models.ClienteForm()
        else:
            if detail_type == 'impianto':
                form = models.ImpiantoForm(initial={'cliente_impianto': models.Cliente.objects.get(pk=cliente_id)})

            if detail_type == 'verifiche':
                form = models.VerificheForm(initial={'verifiche_impianto': models.Impianto.objects.get(pk=impianto_id)})

            if detail_type == 'intervento':
                form = models.InterventoForm(initial={'intervento_impianto': models.Impianto.objects.get(pk=impianto_id)})

        return render(request, 'anagrafe_add.sub', {'header_msg': header_msg, 'data': form,
            'post_url':post_url, 'return_url':return_url})

    if request.method == 'POST':
        if cliente_id is None:
            form = models.ClienteForm(request.POST)
        else:
            if detail_type == 'impianto':
                form = models.ImpiantoForm(request.POST)

            if detail_type == 'verifiche':
                form = models.VerificheForm(request.POST)

            if detail_type == 'intervento':
                form = models.InterventoForm(request.POST)

        if form.is_valid():
            instance = form.save()
            return _display_ok(request, "Ok, record aggiunto.")
            """
            Non funziona correttamente, indagare perchè non va..
            data = view_record(cliente_id=instance.id, detail_type=detail_type,
                    impianto_id=instance.id, sub_impianto_id=instance.id)

            if data is None:
                return _display_error(request, "Qualcosa e' andato storto..")
            return render(request, 'anagrafe_scheda.sub', {'data': data })
            """

        return render(request, 'anagrafe_add.sub', {'header_msg': header_msg, 'data': form,
            'post_url':post_url, 'return_url':return_url})

    return _display_error(request, "Qualcosa e' andato storto..")

def delete_record(request, cliente_id):
    try:
        if request.method == 'GET':
                data = view_record(cliente_id)
                return render(request, 'anagrafe_manager.sub',
                        {'data': data ,
                         'top_message': '<h1>Attenzione! stai per cancellare tutti i dati del seguente cliente.</h1>',
                         'cliente_id': cliente_id})

        if request.method == 'POST':
                cli = database_manager.select_record(models.Cliente.objects, cliente_id)
                nome = cli.nome
                cognome = cli.cognome
                cli.delete()
                s = "Cliente: %s %s Rimosso correttamente." % (nome, cognome)
                return _display_ok(request, s)

    except ObjectDoesNotExist, m:
            return _display_error(request, "Qualcosa e' andato storto..(%s)" % m)

    return _display_error(request, "Qualcosa e' andato storto..")

def edit_record(request, cliente_id):
    if request.method == 'GET':
        if cliente_id != "":
            select = database_manager.select_record(models.Cliente.objects, cliente_id)
            form = models.ClienteForm(instance=select)
            return render(request, 'anagrafe_add.sub', {'action': 'Modifica',
                                                    'cliente_id': cliente_id,
                                                    'cliente': form})
        else:
            return _display_error(request, "Id non trovato.")

    # We manage a post request when we want to save the data.
    if request.method == 'POST':
        #If we found a id take the record to edit it.
        if cliente_id != "":
            select = database_manager.select_record(models.Cliente.objects, cliente_id)
            form = models.ClienteForm(request.POST, instance=select)

        if form.is_valid():
            form.save()
            return _display_scheda(request, cliente_id)
        else:
            return render(request, 'anagrafe_add.sub', {'action': 'Modifica',
                                                        'cliente_id': cliente_id,
                                                        'cliente': form})
    else:
        return _display_error(request, "Id non trovato.")


def detail_record(request, cliente_id, detail_type=None, impianto_id=None, sub_impianto_id=None):

    data = view_record(cliente_id, detail_type, impianto_id, sub_impianto_id)

    if data is None:
        _display_error(request, "Qualcosa e' andato storto!")

    return render(request, 'anagrafe_scheda.sub', {'data': data , 'cliente_id': cliente_id})

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


