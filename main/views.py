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
            dr.urlBar('impianto', ['edit','delete'])
            data += dr.toTable()
        data += data_render.make_url('icon', 'add', 'Aggiungi un impianto..', '/anagrafe/%s/impianto/add', cliente_id)

    elif detail_type == "impianto":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        data += data_render.render_toList(data_to_render[0], data_render.SCHEDA_ANAGRAFE_IMPIANTI, "Dettaglio Impianto")

        if data_to_render[0]['verifiche_id'] != None:
            dr.selectColums(data_render.SCHEDA_ANAGRAFE_VERIFICHE)
            dr.urlBar('verifiche', ['edit','delete'])
            data += dr.toTable()
        data += data_render.make_url('icon', 'add', 'Aggiungi una verifiche a questo impianto..',
                                '/anagrafe/%s/impianto/%s/verifiche/add', cliente_id, impianto_id, sub_impianto_id)

        data += data_render.make_url('icon', 'add', 'Aggiungi un\'intervento a questo impianto..',
                                '/anagrafe/%s/impianto/%s/intervento/add', cliente_id, impianto_id, sub_impianto_id)

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

        return render(request, 'anagrafe_form.sub', {'header_msg': header_msg, 'data': form,
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

        return render(request, 'anagrafe_form.sub', {'header_msg': header_msg, 'data': form,
            'post_url':post_url, 'return_url':return_url})

    return _display_error(request, "Qualcosa e' andato storto..")

def delete_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    try:
        if detail_type is None:
            header_msg = '<h1>Attenzione! stai per cancellare tutti i dati del seguente cliente.</h1>'
            action = '\"Cancella Cliente\"'
            post_url = "%s/delete/" % cliente_id
            return_url = ""

        else:
            if detail_type == 'impianto':
                header_msg = '<h1>Attenzione! stai cancellanodo l\'impianto selezionato.</h1>'
                action = '\"Cancella Impianto\"'
                post_url = "%s/impianto/%s/delete/" % (cliente_id, impianto_id)
                return_url = "%s/" % cliente_id

            if detail_type == 'verifiche':
                header_msg = '<h1>Attenzione! stai cancellanodo la verifica dell\'impianto.</h1>'
                action = '\"Cancella Verifica\"'
                post_url = "%s/impianto/%s/verifiche/%s/delete/" % (cliente_id, impianto_id, sub_impianto_id)
                return_url = "%s/impianto/%s/" % (cliente_id, impianto_id)

            if detail_type == 'intervento':
                header_msg = '<h1>Attenzione! stai cancellanodo l\'intervento dell\'impianto.</h1>'
                action = '\"Cancella Intervento\"'
                post_url = "%s/impianto/%s/intervento/%s/delete/" % (cliente_id, impianto_id, sub_impianto_id)
                return_url = "%s/impianto/%s/" % (cliente_id, impianto_id)

        data = view_record(cliente_id, detail_type, impianto_id, sub_impianto_id)

        if request.method == 'GET':
            return render(request, 'anagrafe_manager.sub', {'header_msg': header_msg,
                'data': data, 'action': action,
                'post_url':post_url, 'return_url':return_url})

        if request.method == 'POST':
            if detail_type is None:
                cli = models.Cliente.objects.get(pk=cliente_id)
                nome = cli.nome
                cognome = cli.cognome
                cli.delete()
                s = "Cliente: %s %s Rimosso correttamente." % (nome, cognome)

            else:
                if detail_type == 'impianto':
                    imp = models.Impianto.objects.get(pk=impianto_id)
                    s = "%s" % imp
                    imp.delete()
                    s = "Impianto: %s rimosso correttamente." % s
                if detail_type == 'verifiche':
                    ver = models.VerificheManutenzione.objects.get(pk=sub_impianto_id)
                    s = "%s" % ver
                    ver.delete()
                    s = "Verifica e Manutezione: %s rimosso correttamente." % s
                if detail_type == 'intervento':
                    interv = models.Intervento.objects.get(pk=sub_impianto_id)
                    s = "%s" % interv
                    interv.delete()
                    s = "Verifica e Manutezione: %s rimosso correttamente." % s

            return _display_ok(request, s)

    except ObjectDoesNotExist, m:
        return _display_error(request, "Qualcosa e' andato storto..(%s)" % m)

    return _display_error(request, "Qualcosa e' andato storto..")


def edit_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    if cliente_id is None:
        return _display_error(request, "Qualcosa e' andato storto..")

    select = None
    if detail_type is None:
        select = models.Cliente.objects.get(pk=cliente_id)
        form = models.ClienteForm(instance=select)
        header_msg = "Modifica Cliente"
        post_url = "%s/edit/" % cliente_id
        return_url = "%s" % cliente_id
    else:
        if detail_type == 'impianto':
            select = models.Impianto.objects.get(pk=impianto_id)
            form = models.ImpiantoForm(instance=select)
            header_msg = "Modifica Impianto"
            post_url = "%s/impianto/%s/edit/" % (cliente_id, impianto_id)
            return_url = "%s/impianto/%s/" % (cliente_id, impianto_id)

        if detail_type == 'verifiche':
            select = models.VerificheManutenzione.objects.get(pk=sub_impianto_id)
            form = models.VerificheForm(instance=select)
            header_msg = "Modifica Verifica e Manutenzione"
            post_url = "%s/impianto/%s/verifiche/%s/edit/" % (cliente_id, impianto_id, sub_impianto_id)
            return_url = "%s/impianto/%s/verifiche/%s/" % (cliente_id, impianto_id, sub_impianto_id)

        if detail_type == 'intervento':
            select = models.Intervento.objects.get(pk=sub_impianto_id)
            form = models.InterventoForm(instance=select)
            header_msg = "Modifica Intervento"
            post_url = "%s/impianto/%s/intervento/%s/edit/" % (cliente_id, impianto_id, sub_impianto_id)
            return_url = "%s/impianto/%s/intervento/%s/" % (cliente_id, impianto_id, sub_impianto_id)

        if detail_type is None:
            return _display_error(request, "Qualcosa e' andato storto..")

    if request.method == 'POST':
        if detail_type is None:
            form = models.ClienteForm(request.POST, instance=select)
        else:
            if detail_type == 'impianto':
                form = models.ImpiantoForm(request.POST, instance=select)

            if detail_type == 'verifiche':
                form = models.VerificheForm(request.POST, instance=select)

            if detail_type == 'intervento':
                form = models.InterventoForm(request.POST, instance=select)

        if form.is_valid():
            instance = form.save()
            return _display_ok(request, "Ok, record aggiornato con successo.")
            """
            Non funziona correttamente, indagare perchè non va..
            data = view_record(cliente_id=instance.id, detail_type=detail_type,
                    impianto_id=instance.id, sub_impianto_id=instance.id)

            if data is None:
                return _display_error(request, "Qualcosa e' andato storto..")
            return render(request, 'anagrafe_scheda.sub', {'data': data })
            """

    return render(request, 'anagrafe_form.sub', {'header_msg': header_msg, 'data': form,
        'post_url':post_url, 'return_url':return_url})

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
            dr.urlBar('cliente', ['edit', 'delete'])
            dr.msgItemsEmpty("<br><h3>La ricerca non ha prodotto risultati.</h3>")
            data += dr.toTable()

    return render(request, 'anagrafe.sub', {'data': data,'form': form })




from main import tools

def populatedb(request):
    data = tools.insert_csv_files(cli_on=False)
    return _display_ok(request, "DB aggiornato con sucesso\n" + data)


