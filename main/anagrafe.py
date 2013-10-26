#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import http
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from main import models
from main import myforms
from main import cfg
from main import tools
from main import data_render
from main import database_manager
from main import scripts
from main import views
from main import users

import re
import logging
logger = logging.getLogger(__name__)


BREADCRUMB_DIVIDER = "<span class=\"divider\">></span>"
BREADCRUMB_ELEMENT = "<li><a href=\"%s\">%s</a>%s</li>"


def __breadcrumbName(l):
    s = "Cliente"
    if "impianto" in l:
        s = "Impianto"
    if "verifica" in l:
        s = "Verifica e Manutenzione"
    elif "intervento" in l:
        s = "Intervento"
    return s

def show_record(request, cliente_id, detail_type=None, impianto_id=None, sub_impianto_id=None, message_hdr='', message='', message_type=''):
    data, data_list = view_record(cliente_id, detail_type, impianto_id, sub_impianto_id)


    # Breadcrumb genarate from current url.
    b = ""
    r = re.compile("\w+\/\d+")
    #['anagrafe/33', 'impianto/33', 'verifica/33']
    l = r.findall(request.path)
    if l:
        url = "/"
        if len(l) > 1:
            for i in l[:-1]:
                url += i + "/"
                s = __breadcrumbName(i)
                b += BREADCRUMB_ELEMENT % (url, s, BREADCRUMB_DIVIDER)

        url += l[-1] + "/"
        s = __breadcrumbName(l[-1])
        b += BREADCRUMB_ELEMENT % (url, s, "")

    if data is None:
        return errors.server_error(request)

    return render(request, 'anagrafe.sub', { 'data': data,
                           'data_list': data_list,
                           'notification': data_render.notification(message_hdr, message, message_type),
                           'scripts':scripts.ANAGRAFE_JS,
                           'breadcrumb': b,
                           })

import gestionale

# TOOLBAR_BTN(url, ico, label)
TOOLBAR_BTN = "<a class=\"btn btn-small btn-info\" id=\"toolbar\" href=\"%s\"><i class=\"%s\"></i> %s</a>"
TOOLBAR_BTN_NAME = "<a class=\"btn btn-small btn-info\" name=\"%s\" value=\"%s\" id=\"toolbar_%s\" href=\"%s\"><i class=\"%s\"></i> %s</a>"
TOOLBAR_ICO_DELETE = "<a name=\"%s\" value=\"%s\" id=\"toolbar_delete\" href=\"%s\"> \
                        <img src=\"%scommon/minus.jpg\" alt=\"delete..\" title=\"delete..\" width=\"16\" height=\"16\"/> </a>"
TOOLBAR_ICO_EDIT = "<a href=\"%s\"><img src=\"%scommon/edit.jpg\" alt=\"edit..\" title=\"edit..\" width=\"16\" height=\"16\"/> </a>"

TOOLBAR_CLIENTE = [
    TOOLBAR_BTN % ("/anagrafe/add/",                         "icon-plus",   "Nuovo"),
    TOOLBAR_BTN % ("/anagrafe/{cliente_id}/edit/",   "icon-pencil", "Modifica"),
    TOOLBAR_BTN_NAME % ("Cliente", "Stai cancellando il cliente, e anche tutti gli impianti, verifiche e interventi relativi.",
            "delete", "/anagrafe/{cliente_id}/delete/", "icon-trash", "Cancella"),
]

TOOLBAR_IMPIANTO = [
    TOOLBAR_BTN % ("/anagrafe/{cliente_id}",                                "icon-arrow-left", "Ritorna"),
    TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/add/",                           "icon-plus",   "Nuovo"),
    TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/{impianto_id}/edit/",   "icon-pencil", "Modifica"),
    TOOLBAR_BTN_NAME % ("Impianto", "Stai cancellando l'impianto selezionato, e anche tutte le verifiche e interventi relativi.",
            "delete", "/anagrafe/{cliente_id}/impianto/{impianto_id}/delete/", "icon-trash", "Cancella"),
]

TOOLBAR_VERIFICA = [
    TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/{impianto_id}",                              "icon-arrow-left", "Ritorna"),
    TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/{impianto_id}/verifica/add/",                 "icon-plus",   "Nuovo"),
    TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/{impianto_id}/verifica/{verifica_id}/edit/",  "icon-pencil", "Modifica"),
    TOOLBAR_BTN_NAME % ("Verifica", "Stai cancellando la verifica selezionata.",
            "delete", "/anagrafe/{cliente_id}/impianto/{impianto_id}/verifica/{verifica_id}/delete/", "icon-trash", "Cancella"),
]

TOOLBAR_INTERVENTO = [
    TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/{impianto_id}",                                    "icon-arrow-left", "Ritorna"),
    TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/{impianto_id}/intervento/add/",                   "icon-plus",   "Nuovo"),
    TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/{impianto_id}/intervento/{intervento_id}/edit/",  "icon-pencil", "Modifica"),
    TOOLBAR_BTN_NAME % ("Intervento", "Stai cancellando l'intervento selezionata.",
            "delete", "/anagrafe/{cliente_id}/impianto/{impianto_id}/intervento/{intervento_id}/delete/", "icon-trash", "Cancella"),
]


def view_record(cliente_id, detail_type=None, impianto_id=None, sub_impianto_id=None, show_title=False, show_cliente=False, show_toolbar=True):
    """
    Data: record table format
    Data_list: record in list format
    Return data, data_list
    """
    if cliente_id == "":
            return None, None

    data = ""
    data_list = ""
    data_to_render = database_manager.search_clienteId(cliente_id)
    if not show_cliente and data_to_render:
        tb=""
        if show_toolbar:
            tb = TOOLBAR_CLIENTE
        data_list = data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_CLIENTE_STD_VIEW, "Dettaglio Cliente",
                toolbar=tb)

    dr = None
    # Show cliente and its impianti
    if detail_type is None:
        data_to_render = database_manager.search_clienteImpiantoSet(cliente_id)
        dr = data_render.DataRender(data_to_render)
        dr.showTitle("Elenco impianti")
        dr.selectColums(cfg.ANAGRAFE_IMPIANTI_STD_VIEW)

        # edit and delete icons with related link
        toolbar_left = [
              TOOLBAR_ICO_EDIT % ("/anagrafe/{cliente_id}/impianto/{impianto_id}/edit/", gestionale.settings.STATIC_URL),
              TOOLBAR_ICO_DELETE % ("Impianto", "Stai cancellando l'impianto selezionato, e anche tutte le verifiche e interventi relativi.",
                  "/anagrafe/{cliente_id}/impianto/{impianto_id}/delete/", gestionale.settings.STATIC_URL),
        ]

        # button to add new Impianto
        if data_to_render:
            toolbar_last = [
                TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/add/", "icon-plus", "Aggiungi un impianto"),
            ]
        else:
            toolbar_last = [
                TOOLBAR_BTN % ("/anagrafe/%s/impianto/add/" % (cliente_id), "icon-plus", "Aggiungi un impianto"),
            ]

        if show_toolbar:
            dr.toolbar(left=toolbar_left, last_row=toolbar_last)

        data += dr.toTable()

    # Show impianto and its verifiche/interventi
    elif detail_type == "impianto":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        if data_to_render:
            data_list += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_IMPIANTI_STD_VIEW, "Dettaglio Impianto",
                    toolbar=TOOLBAR_IMPIANTO)

            # Display all verifiche related to this impianto
            data_to_render = database_manager.search_impiantoVerificaSet(impianto_id)
            dr = data_render.DataRender(data_to_render)
            dr.showTitle("Elenco verifiche")
            dr.selectColums(cfg.ANAGRAFE_VERIFICA_STD_VIEW)
            # edit and delete icons with related link
            toolbar_left = [
                    TOOLBAR_ICO_EDIT % ("/anagrafe/{cliente_id}/impianto/{impianto_id}/verifica/{verifica_id}/edit/", gestionale.settings.STATIC_URL),
                    TOOLBAR_ICO_DELETE % ("Verifica", "Stai cancellando l'intervento selezionata.",
                        "/anagrafe/{cliente_id}/impianto/{impianto_id}/verifica/{verifica_id}/delete/", gestionale.settings.STATIC_URL)
            ]
            # button to add new Verifica
            if data_to_render:
                toolbar_last = [
                        TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/{impianto_id}/verifica/add/", "icon-plus", "Aggiungi una verifica.."),
                ]
            else:
                toolbar_last = [
                    TOOLBAR_BTN % ("/anagrafe/%s/impianto/%s/verifica/add/" % (cliente_id, impianto_id), "icon-plus", "Aggiungi un verifica.."),
                ]

            if show_toolbar:
                dr.toolbar(left=toolbar_left, last_row=toolbar_last)
            data += dr.toTable()


            # Display all intervento related to this impianto
            data_to_render = database_manager.search_impiantoInterventoSet(impianto_id)
            dr = data_render.DataRender(data_to_render)
            dr.showTitle("Elenco interventi")
            dr.selectColums(cfg.ANAGRAFE_INTERVENTI_STD_VIEW)

            # edit and delete icons with related link
            toolbar_left = [
                    TOOLBAR_ICO_EDIT % ("/anagrafe/{cliente_id}/impianto/{impianto_id}/intervento/{intervento_id}/edit/",
                        gestionale.settings.STATIC_URL),
                    TOOLBAR_ICO_DELETE % ("Intervento", "Stai cancellando l'intervento selezionata.",
                        "/anagrafe/{cliente_id}/impianto/{impianto_id}/intervento/{intervento_id}/delete/", gestionale.settings.STATIC_URL)
            ]
            # button to add new Verifica
            if data_to_render:
                toolbar_last = [
                    TOOLBAR_BTN % ("/anagrafe/{cliente_id}/impianto/{impianto_id}/intervento/add/", "icon-plus", "Aggiungi un intervento.."),
                ]
            else:
                toolbar_last = [
                    TOOLBAR_BTN % ("/anagrafe/%s/impianto/%s/intervento/add/" % (cliente_id, impianto_id), "icon-plus", "Aggiungi un intervento.."),
                ]

            if show_toolbar:
                dr.toolbar(left=toolbar_left, last_row=toolbar_last)

            data += dr.toTable()

    elif detail_type == "verifica":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        if data_to_render:
            data_list += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_IMPIANTI_STD_VIEW, "Dettaglio Impianto",
                    toolbar=TOOLBAR_IMPIANTO)

        if sub_impianto_id is not None:
            if data_to_render:
                data_to_render = database_manager.search_verificaId(sub_impianto_id)
                data_list += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_VERIFICA_STD_VIEW, "Dettaglio Verifica e Manutenzioni",
                        toolbar=TOOLBAR_VERIFICA)

    elif detail_type == "intervento":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        if data_to_render:
            data_list += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_IMPIANTI_STD_VIEW, "Dettaglio Impianto",
                        toolbar=TOOLBAR_IMPIANTO)

        if sub_impianto_id is not None:
            data_to_render = database_manager.search_interventoId(sub_impianto_id)
            if data_to_render:
                data_list += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_INTERVENTI_STD_VIEW, "Dettaglio Intervento",
                        toolbar=TOOLBAR_INTERVENTO)
    else:
        data = None
        data_list = None

    return data, data_list


ERROR_DB_HDR = "Database Error."
ERROR_DB_CLIENTE_INSERITO = "Cliente gia\' inserito nel gestionale."
ERROR_DB_DELETE = "Record gia\' rimosso"

ERROR_FORM_HDR = "Errore form."
ERROR_FORM = "Ci sono errori nella compilazione del form."

ERROR_PERM_HDR = "Errore di permesso."
ERROR_PERM_ADD = "Non hai il permesso di Aggiungere record al gestionale."
ERROR_PERM_EDIT = "Non hai il permesso di Modificare il record del gestionale."
ERROR_PERM_DELETE = "Non hai il permesso di Cancellare il record dal gestionale."

OK_DB_DELETE = "Cancellazione riuscita."


def __checkPermission(request, select, form, d):
    if select is None:
        if users.has_addPermission(request, select):
            return True, d

        d['message'] = ERROR_PERM_ADD

    else:
        if users.has_editPermission(request, select):
            return True, d

        d['message'] = ERROR_PERM_EDIT


    d['message_hdr'] = ERROR_PERM_HDR
    d['message_type'] = data_render.MSG_ERROR
    d['form'] = form

    return False, d

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
        'message_hdr':'',
        'message': '',
        'message_type': '',
    }

    if cliente_id is None or detail_type is None:
        msg = None
        form = models.ClienteForm(request.POST, instance=select)
        ret, d = __checkPermission(request, select, form, d)
        if not ret:
            return False, d

        if form.is_valid():
            cli = form.cleaned_data['cliente_id_inserito']
            if cli is not None:
                d['cliente_id'] = cli
                d['message_hdr'] = ERROR_DB_HDR
                d['message'] = ERROR_DB_CLIENTE_INSERITO
                d['message_type'] = data_render.MSG_ERROR
                return True, d

            instance = form.save()
            d['message'] = msg
            d['cliente_id'] = instance.id
            return True, d

        else:
            d['message'] = ERROR_FORM
            d['message_hdr'] = ERROR_FORM_HDR
            d['message_type'] = data_render.MSG_ERROR
            d['form'] = form
            return False, d
    else:
        if detail_type == 'impianto':
            form = models.ImpiantoForm(request.POST, instance=select)
            ret, d = __checkPermission(request, select, form, d)
            if not ret:
                return False, d

            if form.is_valid():
                instance = form.save()
                d['cliente_id'] = cliente_id
                d['impianto_id'] = instance.id
                return True, d
            else:
                d['form'] = form
                d['message'] = ERROR_FORM
                d['message_hdr'] = ERROR_FORM_HDR
                d['message_type'] = data_render.MSG_ERROR
                d['form'] = form
                return False, d

        if detail_type == 'verifica':
            form = models.VerificaForm(request.POST, instance=select)
            ret, d = __checkPermission(request, select, form, d)
            if not ret:
                return False, d

            if form.is_valid():
                instance = form.save()
                d['cliente_id'] = cliente_id
                d['impianto_id'] = impianto_id
                d['sub_impianto_id'] = instance.id
                d['detail_type'] = detail_type
                return True, d
            else:
                d['form'] = form
                d['message'] = ERROR_FORM
                d['message_hdr'] = ERROR_FORM_HDR
                d['message_type'] = data_render.MSG_ERROR
                return False, d

        if detail_type == 'intervento':
            form = models.InterventoForm(request.POST, instance=select)
            ret, d = __checkPermission(request, select, form, d)
            if not ret:
                return False, d

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
                d['form'] = form
                d['message'] = ERROR_FORM
                d['message_hdr'] = ERROR_FORM_HDR
                d['message_type'] = data_render.MSG_ERROR
                return False, d

    return errors.server_error(request)

def add_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    script = ""
    data = ""
    data_list = ""
    notification = ""
    if cliente_id is None:
        header_msg = "Aggiungi Nuovo Cliente"
        post_url = "add/"
    else:
        if detail_type == 'impianto':
            header_msg = "Aggiungi Nuovo Impianto"
            post_url = "%s/impianto/add/" % cliente_id

        if detail_type == 'verifica':
            header_msg = "Aggiungi Nuova Verifica e Manutenzione"
            post_url = "%s/impianto/%s/verifica/add/" % (cliente_id, impianto_id)

        if detail_type == 'intervento':
            header_msg = "Aggiungi Nuovo Intervento"
            post_url = "%s/impianto/%s/intervento/add/" % (cliente_id, impianto_id)

        if detail_type is None:
            return errors.server_error(request)

    if request.method == 'GET':
        if cliente_id is None:
            form = models.ClienteForm()
        else:
            if detail_type == 'impianto':
                form = models.ImpiantoForm(initial={'cliente_impianto': models.Cliente.objects.get(pk=cliente_id)})
                script = scripts.IMPIANTO_JS
                data, data_list = view_record(cliente_id, detail_type, impianto_id)

            if detail_type == 'verifica':
                form = models.VerificaForm(initial={'verifica_impianto': models.Impianto.objects.get(pk=impianto_id)})
                script = scripts.VERIFICA_JS
                data, data_list = view_record(cliente_id, detail_type, impianto_id)

            if detail_type == 'intervento':
                form = models.InterventoForm(initial={'intervento_impianto': models.Impianto.objects.get(pk=impianto_id)})
                script = scripts.INTERVENTO_JS
                data, data_list = view_record(cliente_id, detail_type, impianto_id)

    if request.method == 'POST':
        ret, d = __editAdd_record(cliente_id, impianto_id, sub_impianto_id, detail_type, request)
        if ret:
            return show_record(**d)
        else:
            request = d['request']
            form = d['form']
            notification = data_render.notification(d['message_hdr'], d['message'], d['message_type'])

    return render(request, 'anagrafe_form.sub', {'notification': notification, 'header_msg': data_render.TITLE_STYLE_FORM % header_msg,
        'data_forms': form, 'data':data, 'scripts': script, 'post_url':post_url})


def edit_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    if cliente_id is None:
        return errors.server_error(request)

    select = None
    data = ""
    data_list = ""
    script = ""
    notification = ""
    if detail_type is None:
        select = models.Cliente.objects.get(pk=cliente_id)
        form = models.ClienteForm(instance=select)
        header_msg = "Modifica Cliente"
        post_url = "%s/edit/" % cliente_id
    else:
        if detail_type == 'impianto':
            select = models.Impianto.objects.get(pk=impianto_id)
            form = models.ImpiantoForm(instance=select)
            header_msg = "Modifica Impianto"
            post_url = "%s/impianto/%s/edit/" % (cliente_id, impianto_id)
            script = scripts.IMPIANTO_JS

        if detail_type == 'verifica':
            select = models.Verifica.objects.get(pk=sub_impianto_id)
            form = models.VerificaForm(instance=select)
            header_msg = "Modifica Verifica e Manutenzione"
            post_url = "%s/impianto/%s/verifica/%s/edit/" % (cliente_id, impianto_id, sub_impianto_id)
            script = scripts.VERIFICA_JS
            data, data_list = view_record(cliente_id, detail_type, impianto_id)

        if detail_type == 'intervento':
            select = models.Intervento.objects.get(pk=sub_impianto_id)
            form = models.InterventoForm(instance=select)
            header_msg = "Modifica Intervento"
            post_url = "%s/impianto/%s/intervento/%s/edit/" % (cliente_id, impianto_id, sub_impianto_id)
            script = scripts.INTERVENTO_JS

        if detail_type is None:
            return errors.server_error(request)

    if request.method == 'POST':
        ret, d = __editAdd_record(cliente_id, impianto_id, sub_impianto_id, detail_type, request, select=select)
        if ret:
            return show_record(**d)
        else:
            request = d['request']
            form = d['form']
            notification = data_render.notification(d['message_hdr'], d['message'], d['message_type'])

    return render(request, 'anagrafe_form.sub', {'notification': notification, 'header_msg': data_render.TITLE_STYLE_FORM % header_msg,
        'data_forms': form, 'data':data, 'scripts': script, 'post_url':post_url})

def delete_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    data = ''
    d = ''
    data_list = ''
    try:
        if request.method == 'POST':
            if not users.has_deletePermission(request):
                return show_record(request, cliente_id=cliente_id, detail_type=detail_type, impianto_id=impianto_id, sub_impianto_id=sub_impianto_id,
                        message_hdr=ERROR_PERM_HDR, message=ERROR_PERM_DELETE, message_type=data_render.MSG_ERROR)

            if detail_type is None:
                cli = models.Cliente.objects.get(pk=cliente_id)
                nome = cli.nome
                cognome = cli.cognome
                cli.delete()
                s = "Cliente: %s %s Rimosso correttamente." % (nome, cognome)
                d = {
                    'message_hdr': OK_DB_DELETE ,
                    'message': s,
                    'message_type':data_render.MSG_OK,
                 }

                return views.home(request, d)

            else:
                if detail_type == 'impianto':
                    imp = models.Impianto.objects.get(pk=impianto_id)
                    s = "%s" % imp
                    imp.delete()
                    s = "Impianto: %s rimosso correttamente." % s
                    return show_record(request, cliente_id=cliente_id,
                            message_hdr=OK_DB_DELETE, message=s, message_type=data_render.MSG_OK)

                if detail_type == 'verifica':
                    ver = models.Verifica.objects.get(pk=sub_impianto_id)
                    s = "%s" % ver
                    ver.delete()
                    s = "Verifica e Manutezione: %s rimosso correttamente." % s
                    return show_record(request, cliente_id=cliente_id, impianto_id=impianto_id,
                            message_hdr=OK_DB_DELETE, message=s, message_type=data_render.MSG_OK)

                if detail_type == 'intervento':
                    interv = models.Intervento.objects.get(pk=sub_impianto_id)
                    s = "%s" % interv
                    interv.delete()
                    s = "Verifica e Manutezione: %s rimosso correttamente." % s
                    return show_record(request, cliente_id=cliente_id, impianto_id=impianto_id,
                            message_hdr=OK_DB_DELETE, message=s, message_type=data_render.MSG_OK)

    except ObjectDoesNotExist, m:
        return show_record(request, cliente_id=cliente_id, detail_type=detail_type, impianto_id=impianto_id, sub_impianto_id=sub_impianto_id,
                message_hdr=ERROR_DB_HDR, message=ERROR_DB_DELETE, message_type=data_render.MSG_ERROR)

    return errors.server_error(request)



def detail_record(request, cliente_id, detail_type=None, impianto_id=None, sub_impianto_id=None):
    return show_record(request, cliente_id, detail_type, impianto_id, sub_impianto_id)


def anagrafe(request):
    form = myforms.FullTextSearchForm()
    data = ''

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

    return render(request, 'anagrafe.sub',{'query_path':request.get_full_path(),
                                           'data': data,
                                           'data_form': form,
                                           'scripts': '',
                                           })

