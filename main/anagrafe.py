#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import http
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from main import models
from main import myforms
from main import cfg
from main import tools
from main import data_render
from main import database_manager
from main import scripts

import logging
logger = logging.getLogger(__name__)

def _display_error(request, msg):
    logger.error("%s" % msg)
    return render(request, 'messages.sub',
            { 'msg_hdr':'Error!',
              'msg_body': msg })

def _display_ok(request, msg):
    logger.info("%s" % msg)
    return render(request, 'messages.sub',
            { 'msg_hdr':'Ok!',
              'msg_body': msg})


def show_record(request, cliente_id, detail_type=None, impianto_id=None, sub_impianto_id=None, message=None):
    data = scripts.SHOW_ADD_JS
    data += view_record(cliente_id, detail_type, impianto_id, sub_impianto_id)

    if data is None:
        _display_error(request, "Qualcosa e' andato storto!")

    return render(request, 'anagrafe_scheda.sub', {'data': data,
                           'top_message': message,
                           'cliente_id': cliente_id,
                           'detail_type': detail_type,
                           'impianto_id': impianto_id,
                           'sub_impianto_id': sub_impianto_id})

TOOLBAR_CLIENTE = [
    "<a id=\"toolbar\" href=\"/anagrafe/add\">add</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/edit#cliente\">edit</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/delete#cliente\">delete</a>",
]

TOOLBAR_IMPIANTO = [
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>#cliente\">cliente</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/add\">add</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/edit#impianto\">edit</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/delete#impianto\">delete</a>",
]

TOOLBAR_VERIFICA = [
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>#impianto\">impianto</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/verifica/add#verifica\">add</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/verifica/<verifica_id>/edit#verifica\">edit</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/verifica/<verifica_id>/delete#verifica\">delete</a>",
]

TOOLBAR_INTERVENTO = [
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>#impianto\">impianto</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/intervento/add#intervento\">add</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/intervento/<intervento_id>/edit#intervento\">edit</a>",
    "<a id=\"toolbar\" href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/intervento/<intervento_id>/delete#intervento\">delete</a>",
]

def view_record(cliente_id, detail_type=None, impianto_id=None, sub_impianto_id=None, show_cliente=False):
    if cliente_id == "":
            return None

    data = ""
    data_to_render = database_manager.search_clienteId(cliente_id)
    if not show_cliente:
        data = data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_CLIENTE_STD_VIEW, "<a id=\"cliente\">Dettaglio Cliente</a>",
                toolbar=TOOLBAR_CLIENTE)

    dr = None
    # Show cliente and its impianti
    if detail_type is None:
        data_to_render = database_manager.search_clienteImpiantoSet(cliente_id)
        dr = data_render.DataRender(data_to_render)
        dr.selectColums(cfg.ANAGRAFE_IMPIANTI_STD_VIEW)
        # edit and delete icons with related link
        tb_left = [
              "<a href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/edit#impianto\"> \
                <img src=\"/static/edit.jpg\" alt=\"edit..\" title=\"edit..\" width=\"16\" height=\"16\"/> </a>",
              "<a href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/delete#impianto\"> \
                <img src=\"/static/minus.jpg\" alt=\"delete..\" title=\"delete..\" width=\"16\" height=\"16\"/> </a>",
        ]

        # button to add new Impianto
        if data_to_render:
            tb_last = [
                "<a href=\"/anagrafe/<cliente_id>/impianto/add\" name=\"href_button\">Aggiungi un impianto..</a>",
            ]
            dr.toolbar(left=tb_left, last_row=tb_last)
        else:
            tb_last_row = [
                  "<a href=\"/anagrafe/%s/impianto/add\" name=\"href_button\">Aggiungi un impianto..</a>" % (cliente_id)
            ]
            dr.toolbar(last_row=tb_last_row)
        data += dr.toTable()

    # Show impianto and its verifiche/interventi
    elif detail_type == "impianto":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        data += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_IMPIANTI_STD_VIEW, "<a id=\"impianto\">Dettaglio Impianto</a>",
                toolbar=TOOLBAR_IMPIANTO)

        # Display all verifiche related to this impianto
        data_to_render = database_manager.search_impiantoVerificaSet(impianto_id)
        dr = data_render.DataRender(data_to_render)
        dr.selectColums(cfg.ANAGRAFE_VERIFICA_STD_VIEW)
        # edit and delete icons with related link
        tb_left = [
              "<a href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/verifica/<verifica_id>/edit#verifica\"> \
                <img src=\"/static/edit.jpg\" alt=\"edit..\" title=\"edit..\" width=\"16\" height=\"16\"/> </a>",
              "<a href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/verifica/<verifica_id>/delete#verifica\"> \
                <img src=\"/static/minus.jpg\" alt=\"delete..\" title=\"delete..\" width=\"16\" height=\"16\"/> </a>",
        ]
        # button to add new Verifica
        if data_to_render:
            tb_last = [
                  "<a href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/verifica/add#verifica\" name=\"href_button\">Aggiungi una verifica..</a>",
            ]
            dr.toolbar(left=tb_left, last_row=tb_last)
        else:
            tb_last_row = [
                  "<a href=\"/anagrafe/%s/impianto/%s/verifica/add#verifica\" name=\"href_button\">Aggiungi una verifica..</a>" % (cliente_id, impianto_id)
            ]
            dr.toolbar(last_row=tb_last_row)
        data += dr.toTable()


        # Display all intervento related to this impianto
        data_to_render = database_manager.search_impiantoInterventoSet(impianto_id)
        dr = data_render.DataRender(data_to_render)
        dr.selectColums(cfg.ANAGRAFE_INTERVENTI_STD_VIEW)

        # edit and delete icons with related link
        tb_left = [
              "<a href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/intervento/<intervento_id>/edit#intervento\"> \
                <img src=\"/static/edit.jpg\" alt=\"edit..\" title=\"edit..\" width=\"16\" height=\"16\"/> </a>",
              "<a href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/intervento/<intervento_id>/delete#intervento\"> \
                <img src=\"/static/minus.jpg\" alt=\"delete..\" title=\"delete..\" width=\"16\" height=\"16\"/> </a>",
        ]
        # button to add new Verifica
        if data_to_render:
            tb_last = [
                  "<a href=\"/anagrafe/<cliente_id>/impianto/<impianto_id>/intervento/add#intervento\" name=\"href_button\">Aggiungi un intervento..</a>",
            ]
            dr.toolbar(left=tb_left, last_row=tb_last)
        else:
            tb_last_row = [
                  "<a href=\"/anagrafe/%s/impianto/%s/intervento/add#intervento\" name=\"href_button\">Aggiungi un intervento..</a>" % (cliente_id, impianto_id)
            ]
            dr.toolbar(last_row=tb_last_row)
        data += dr.toTable()


    elif detail_type == "verifica":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        data += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_IMPIANTI_STD_VIEW, "Dettaglio Impianto",
                toolbar=TOOLBAR_IMPIANTO)

        if sub_impianto_id is not None:
            if data_to_render:
                data_to_render = database_manager.search_verificaId(sub_impianto_id)
                data += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_VERIFICA_STD_VIEW, "<a id=\"verifica\">Dettaglio Verifica e Manutenzioni</a>",
                        toolbar=TOOLBAR_VERIFICA)

    elif detail_type == "intervento":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        data += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_IMPIANTI_STD_VIEW, "Dettaglio Impianto",
                    toolbar=TOOLBAR_IMPIANTO)

        if sub_impianto_id is not None:
            data_to_render = database_manager.search_interventoId(sub_impianto_id)
            if data_to_render:
                data += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_INTERVENTI_STD_VIEW, "<a id=\"intervento\">Dettaglio Intervento</a>",
                        toolbar=TOOLBAR_INTERVENTO)
    else:
        data = None

    return data

def _intervento_cfg(cliente_id, detail_type, impianto_id):
    data = scripts.INTERVENTO_ADD_JS
    data += view_record(cliente_id, detail_type, impianto_id, show_cliente=True)
    return data

def _verifica_cfg(cliente_id, detail_type, impianto_id):
    data = scripts.VERIFICA_ADD_JS
    data += view_record(cliente_id, detail_type, impianto_id, show_cliente=True)
    return data

def _impianto_cfg(cliente_id, detail_type, impianto_id):
    data = scripts.IMPIANTO_ADD_JS
    return data

def __editAdd_record(cliente_id, impianto_id, sub_impianto_id, detail_type, request, select=None):
    """
    return dict
    request, cliente_id, detail_type=None, impianto_id=None, sub_impianto_id=None, message=None
    """
    d = {
        'request':request,
        'detail_type':None,
        'cliente_id':None,
        'impianto_id':None,
        'sub_impianto_id':None,
        'message':None,
    }

    if cliente_id is None or detail_type is None:
        msg=None
        form = models.ClienteForm(request.POST, instance=select)
        if form.is_valid():
            cli = form.cleaned_data['cliente_id_inserito']
            if cli is not None:
                d['cliente_id'] = cli
                d['message'] = "<h1>Cliente gia\' inserito nel gestionale</h1>"
                return True, d

            instance = form.save()
            d['message'] = msg
            d['cliente_id'] = instance.id
            return True, d

        else:
            d['form'] = form
            return False, d

    else:
        if detail_type == 'impianto':
            form = models.ImpiantoForm(request.POST, instance=select)
            if form.is_valid():
                instance = form.save()
                d['cliente_id'] = cliente_id
                d['impianto_id'] = instance.id
                return True, d
            else:
                d['message'] = "Errore nel form"
                d['form'] = form
                return False, d

        if detail_type == 'verifica':
            form = models.VerificaForm(request.POST, instance=select)
            if form.is_valid():
                instance = form.save()
                d['cliente_id'] = cliente_id
                d['impianto_id'] = impianto_id
                d['sub_impianto_id'] = instance.id
                d['detail_type'] = detail_type
                return True, d
            else:
                d['form'] = form
                d['message'] = "Errore nel form"
                return False, d

        if detail_type == 'intervento':
            form = models.InterventoForm(request.POST, instance=select)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.tipo_intervento = instance.tipo_intervento.capitalize()
                instance.save()
                d['cliente_id'] = cliente_id
                d['impianto_id'] = impianto_id
                d['sub_impianto_id'] = instance.id
                d['detail_type'] = detail_type
                return True, d
            else:
                d['message'] = "Errore nel form"
                d['form'] = form
                return False, d

    return _display_error(request, "Qualcosa e' andato storto..")

def add_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    data = scripts.RECORDADD_ADD_JS
    if cliente_id is None:
        header_msg = "Aggiungi Nuovo Cliente"
        post_url = "add/"
    else:
        if detail_type == 'impianto':
            header_msg = "<a id=\"impianto\">Aggiungi Nuovo Impianto</a>"
            post_url = "%s/impianto/add/" % cliente_id

        if detail_type == 'verifica':
            header_msg = "<a id=\"verifica\">Aggiungi Nuova Verifica e Manutenzione</a>"
            post_url = "%s/impianto/%s/verifica/add/" % (cliente_id, impianto_id)

        if detail_type == 'intervento':
            header_msg = "<a id=\"intervento\">Aggiungi Nuovo Intervento</a>"
            post_url = "%s/impianto/%s/intervento/add/" % (cliente_id, impianto_id)

        if detail_type is None:
            return _display_error(request, "Qualcosa e' andato storto..")

    if request.method == 'GET':
        if cliente_id is None:
            form = models.ClienteForm()
        else:
            if detail_type == 'impianto':
                form = models.ImpiantoForm(initial={'cliente_impianto': models.Cliente.objects.get(pk=cliente_id)})
                data = _impianto_cfg(cliente_id, detail_type, impianto_id)

            if detail_type == 'verifica':
                form = models.VerificaForm(initial={'verifica_impianto': models.Impianto.objects.get(pk=impianto_id)})
                data = _verifica_cfg(cliente_id, detail_type, impianto_id)

            if detail_type == 'intervento':
                form = models.InterventoForm(initial={'intervento_impianto': models.Impianto.objects.get(pk=impianto_id)})
                data = _intervento_cfg(cliente_id, detail_type, impianto_id)

    if request.method == 'POST':
        ret, d = __editAdd_record(cliente_id, impianto_id, sub_impianto_id, detail_type, request)
        if ret:
            return show_record(**d)
        else:
            request = d['request']
            form = d['form']

    return render(request, 'anagrafe_form.sub', {'header_msg': header_msg, 'data_forms': form,
        'data':data, 'post_url':post_url})


def edit_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    if cliente_id is None:
        return _display_error(request, "Qualcosa e' andato storto..")

    select = None
    data = scripts.EDIT_ADD_JS
    if detail_type is None:
        select = models.Cliente.objects.get(pk=cliente_id)
        form = models.ClienteForm(instance=select)
        header_msg = "Modifica Cliente"
        post_url = "%s/edit/" % cliente_id
    else:
        if detail_type == 'impianto':
            select = models.Impianto.objects.get(pk=impianto_id)
            form = models.ImpiantoForm(instance=select)
            header_msg = "<a id=\"impianto\">Modifica Impianto</a>"
            post_url = "%s/impianto/%s/edit/" % (cliente_id, impianto_id)

        if detail_type == 'verifica':
            select = models.Verifica.objects.get(pk=sub_impianto_id)
            form = models.VerificaForm(instance=select)
            header_msg = "<a id=\"verifica\">Modifica Verifica e Manutenzione</a>"
            post_url = "%s/impianto/%s/verifica/%s/edit/" % (cliente_id, impianto_id, sub_impianto_id)
            data = _verifica_cfg(cliente_id, detail_type, impianto_id)

        if detail_type == 'intervento':
            select = models.Intervento.objects.get(pk=sub_impianto_id)
            form = models.InterventoForm(instance=select)
            header_msg = "<a id=\"intervento\">Modifica Intervento</a>"
            post_url = "%s/impianto/%s/intervento/%s/edit/" % (cliente_id, impianto_id, sub_impianto_id)

        if detail_type is None:
            return _display_error(request, "Qualcosa e' andato storto..")

    if request.method == 'POST':
        ret, d = __editAdd_record(cliente_id, impianto_id, sub_impianto_id, detail_type, request, select=select)
        if ret:
            return show_record(**d)
        else:
            request = d['request']
            form = d['form']

    return render(request, 'anagrafe_form.sub', {'header_msg': header_msg, 'data_forms': form,
        'data':data, 'post_url':post_url})

def delete_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    data = scripts.DELETE_ADD_JS
    try:
        if detail_type is None:
            header_msg = '<h1>Attenzione! stai per cancellare tutti i dati del seguente cliente.</h1>'
            action = '\"Cancella Cliente\"'
            post_url = "%s/delete/" % cliente_id
        else:
            if detail_type == 'impianto':
                header_msg = '<h1>Attenzione! stai cancellanodo l\'impianto selezionato.</h1>'
                action = '\"Cancella Impianto\"'
                post_url = "%s/impianto/%s/delete/" % (cliente_id, impianto_id)

            if detail_type == 'verifica':
                header_msg = '<h1>Attenzione! stai cancellanodo la verifica dell\'impianto.</h1>'
                action = '\"Cancella Verifica\"'
                post_url = "%s/impianto/%s/verifica/%s/delete/" % (cliente_id, impianto_id, sub_impianto_id)

            if detail_type == 'intervento':
                header_msg = '<h1>Attenzione! stai cancellanodo l\'intervento dell\'impianto.</h1>'
                action = '\"Cancella Intervento\"'
                post_url = "%s/impianto/%s/intervento/%s/delete/" % (cliente_id, impianto_id, sub_impianto_id)

        data += view_record(cliente_id, detail_type, impianto_id, sub_impianto_id)

        if request.method == 'GET':
            return render(request, 'anagrafe_manager.sub', {'header_msg': header_msg,
                'data': data, 'action': action,
                'post_url':post_url})

        if request.method == 'POST':
            if detail_type is None:
                cli = models.Cliente.objects.get(pk=cliente_id)
                nome = cli.nome
                cognome = cli.cognome
                cli.delete()
                s = "Cliente: %s %s Rimosso correttamente." % (nome, cognome)

                return _display_ok(request, s)

            else:
                if detail_type == 'impianto':
                    imp = models.Impianto.objects.get(pk=impianto_id)
                    s = "%s" % imp
                    imp.delete()
                    s = "Impianto: %s rimosso correttamente." % s
                    return show_record(request, cliente_id=cliente_id, message=s)

                if detail_type == 'verifica':
                    ver = models.Verifica.objects.get(pk=sub_impianto_id)
                    s = "%s" % ver
                    ver.delete()
                    s = "Verifica e Manutezione: %s rimosso correttamente." % s
                    return show_record(request, cliente_id=cliente_id, impianto_id=impianto_id, message=s)

                if detail_type == 'intervento':
                    interv = models.Intervento.objects.get(pk=sub_impianto_id)
                    s = "%s" % interv
                    interv.delete()
                    s = "Verifica e Manutezione: %s rimosso correttamente." % s
                    return show_record(request, cliente_id=cliente_id, impianto_id=impianto_id, message=s)

            return _display_ok(request, s)

    except ObjectDoesNotExist, m:
        return _display_error(request, "Qualcosa e' andato storto..(%s)" % m)

    return _display_error(request, "Qualcosa e' andato storto..")



def detail_record(request, cliente_id, detail_type=None, impianto_id=None, sub_impianto_id=None):
    return show_record(request, cliente_id, detail_type, impianto_id, sub_impianto_id)


def anagrafe(request):
    form = myforms.FullTextSearchForm()
    data = scripts.HOME_ADD_JS

    search_string = ""
    data_to_render = []
    order_by_field = ""
    ordering = ""

    form_dict = {
            'search_keys' : "",
            'order_by_field' : "",
            'ordering' : "",
    }

    if request.method == 'GET' and request.GET != {}:
            form = myforms.FullTextSearchForm(request.GET)
            if form.is_valid():
                    form_dict['search_keys'] = form.cleaned_data['search_keys']
                    form_dict['order_by_field'] = form.cleaned_data['order_by_field']
                    form_dict['ordering'] = form.cleaned_data['ordering']

            data_to_render = database_manager.search_fullText(**form_dict)
            dr = data_render.DataRender(data_to_render)
            dr.selectColums(cfg.ANAGRAFE_STD_VIEW)

            dr.msgItemsEmpty("<br><h3>La ricerca non ha prodotto risultati.</h3>")
            if search_string != "":
                dr.msgStatistics(("<br><h2>\"%s\" trovati:" % search_string) + " %s</h2><br>")
            dr.showStatistics()
            dr.orderUrl('anagrafe', form_dict)
            data += dr.toTable()

    return render(request, 'anagrafe.sub', {'query_path':request.get_full_path(), 'data': data,'data_form': form})

