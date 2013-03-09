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

def view_record(cliente_id, detail_type=None, impianto_id=None, sub_impianto_id=None, show_cliente=False):
    if cliente_id == "":
            return None

    data = ""
    data_to_render = database_manager.search_clienteId(cliente_id)
    if not show_cliente:
        data = data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_CLIENTE_STD_VIEW, "<a id=\"cliente\">Dettaglio Cliente</a>")

    dr = data_render.DataRender(data_to_render)

    if detail_type is None:
        if len(data_to_render) >= 1 and data_to_render[0]['impianto_id'] != None:
            dr.selectColums(cfg.ANAGRAFE_IMPIANTI_STD_VIEW)
            dr.urlBar('impianto', ['edit','delete'])
            dr.uniqueRow()
            data += dr.toTable()
        data += data_render.make_url('button', 'add', 'Aggiungi un impianto..', '/anagrafe/%s/impianto/add', cliente_id)

    elif detail_type == "impianto":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        data += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_IMPIANTI_STD_VIEW, "<a id=\"impianto\">Dettaglio Impianto</a>", 'cliente')

        if data_to_render[0]['verifica_id'] != None:
            dr.selectColums(cfg.ANAGRAFE_VERIFICA_STD_VIEW)
            dr.urlBar('verifica', ['edit','delete'])
            data += dr.toTable()

        if data_to_render[0]['intervento_id'] != None:
            dr.selectColums(cfg.ANAGRAFE_INTERVENTI_STD_VIEW)
            dr.urlBar('intervento', ['edit','delete'])
            data += dr.toTable()

        data += data_render.make_url('button', 'add', 'Aggiungi una verifica a questo impianto..',
                                '/anagrafe/%s/impianto/%s/verifica/add#verifica', cliente_id, impianto_id, sub_impianto_id)

        data += data_render.make_url('button', 'add', 'Aggiungi un\'intervento a questo impianto..',
                                '/anagrafe/%s/impianto/%s/intervento/add#intervento', cliente_id, impianto_id, sub_impianto_id)

    elif detail_type == "verifica":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        data += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_IMPIANTI_STD_VIEW, "Dettaglio Impianto", 'cliente')

        if sub_impianto_id is not None:
            data_to_render = database_manager.search_verificaId(sub_impianto_id)
            data += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_VERIFICA_STD_VIEW, "<a id=\"verifica\">Dettaglio Verifica e Manutenzioni</a>", 'impianto')

    elif detail_type == "intervento":
        data_to_render = database_manager.search_impiantoId(impianto_id)
        data += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_IMPIANTI_STD_VIEW, "Dettaglio Impianto", 'cliente')

        if sub_impianto_id is not None:
            data_to_render = database_manager.search_interventoId(sub_impianto_id)
            data += data_render.render_toList(data_to_render[0], cfg.ANAGRAFE_INTERVENTI_STD_VIEW, "<a id=\"intervento\">Dettaglio Intervento</a>", 'impianto')
    else:
        data = None

    return data

def _verifica_cfg(cliente_id, detail_type, impianto_id):
    data = scripts.VERIFICA_ADD_JS
    data += view_record(cliente_id, detail_type, impianto_id, show_cliente=True)
    return data

def _impianto_cfg(cliente_id, detail_type, impianto_id):
    data = scripts.IMPIANTO_ADD_JS
    return data

def __editAdd_record(cliente_id, impianto_id, sub_impianto_id, detail_type, request, select=None):
    if cliente_id is None or detail_type is None:
        msg=None
        form = models.ClienteForm(request.POST, instance=select)
        if form.is_valid():
            cli = form.cleaned_data['cliente_id_inserito']
            if cli is not None:
                return show_record(request, cliente_id=cli, message="<h1>Cliente gia\' inserito nel gestionale</h1>")

            instance = form.save()
            return show_record(request, cliente_id=instance.id, message=msg)

    else:
        if detail_type == 'impianto':
            form = models.ImpiantoForm(request.POST, instance=select)
            if form.is_valid():
                instance = form.save()
                return show_record(request, cliente_id=cliente_id, impianto_id=instance.id)

        if detail_type == 'verifica':
            form = models.VerificaForm(request.POST, instance=select)
            if form.is_valid():
                instance = form.save()
                return show_record(request, cliente_id=cliente_id, impianto_id=impianto_id,
                        detail_type=detail_type, sub_impianto_id=instance.id)

        if detail_type == 'intervento':
            form = models.InterventoForm(request.POST, instance=select)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.tipo_intervento = instance.tipo_intervento.capitalize()
                instance.save()
                return show_record(request, cliente_id=cliente_id, impianto_id=impianto_id,
                        detail_type=detail_type, sub_impianto_id=instance.id)

    return _display_error(request, "Qualcosa e' andato storto..")

def add_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    data = scripts.RECORDADD_ADD_JS
    if cliente_id is None:
        header_msg = "Aggiungi Nuovo Cliente"
        post_url = "add/"
        return_url = "/#cliente"
    else:
        if detail_type == 'impianto':
            header_msg = "<a id=\"impianto\">Aggiungi Nuovo Impianto</a>"
            post_url = "%s/impianto/add/" % cliente_id
            return_url = "/anagrafe/%s/#impianto" % cliente_id

        if detail_type == 'verifica':
            header_msg = "<a id=\"verifica\">Aggiungi Nuova Verifica e Manutenzione</a>"
            post_url = "%s/impianto/%s/verifica/add/" % (cliente_id, impianto_id)
            return_url = "/anagrafe/%s/impianto/%s/#verifica" % (cliente_id, impianto_id)

        if detail_type == 'intervento':
            header_msg = "<a id=\"intervento\">Aggiungi Nuovo Intervento</a>"
            post_url = "%s/impianto/%s/intervento/add/" % (cliente_id, impianto_id)
            return_url = "/anagrafe/%s/impianto/%s/#intervento" % (cliente_id, impianto_id)

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

    if request.method == 'POST':
        return __editAdd_record(cliente_id, impianto_id, sub_impianto_id, detail_type, request)

    return render(request, 'anagrafe_form.sub', {'header_msg': header_msg, 'data_forms': form,
        'data':data, 'post_url':post_url, 'return_url':return_url})


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
        return_url = "/anagrafe/%s/#cliente" % cliente_id
    else:
        if detail_type == 'impianto':
            select = models.Impianto.objects.get(pk=impianto_id)
            form = models.ImpiantoForm(instance=select)
            header_msg = "<a id=\"impianto\">Modifica Impianto</a>"
            post_url = "%s/impianto/%s/edit/" % (cliente_id, impianto_id)
            return_url = "/anagrafe/%s/impianto/%s/#impianto" % (cliente_id, impianto_id)

        if detail_type == 'verifica':
            select = models.Verifica.objects.get(pk=sub_impianto_id)
            form = models.VerificaForm(instance=select)
            header_msg = "<a id=\"verifica\">Modifica Verifica e Manutenzione</a>"
            post_url = "%s/impianto/%s/verifica/%s/edit/" % (cliente_id, impianto_id, sub_impianto_id)
            return_url = "/anagrafe/%s/impianto/%s/verifica/%s/#verifica" % (cliente_id, impianto_id, sub_impianto_id)
            data = _verifica_cfg(cliente_id, detail_type, impianto_id)

        if detail_type == 'intervento':
            select = models.Intervento.objects.get(pk=sub_impianto_id)
            form = models.InterventoForm(instance=select)
            header_msg = "<a id=\"intervento\">Modifica Intervento</a>"
            post_url = "%s/impianto/%s/intervento/%s/edit/" % (cliente_id, impianto_id, sub_impianto_id)
            return_url = "/anagrafe/%s/impianto/%s/intervento/%s/#intervento" % (cliente_id, impianto_id, sub_impianto_id)

        if detail_type is None:
            return _display_error(request, "Qualcosa e' andato storto..")

    if request.method == 'POST':
        return __editAdd_record(cliente_id, impianto_id, sub_impianto_id, detail_type, request, select=select)

    return render(request, 'anagrafe_form.sub', {'header_msg': header_msg, 'data_forms': form,
        'data':data, 'post_url':post_url, 'return_url':return_url})

def delete_record(request, cliente_id=None, detail_type=None, impianto_id=None, sub_impianto_id=None):
    data = scripts.DELETE_ADD_JS
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

            if detail_type == 'verifica':
                header_msg = '<h1>Attenzione! stai cancellanodo la verifica dell\'impianto.</h1>'
                action = '\"Cancella Verifica\"'
                post_url = "%s/impianto/%s/verifica/%s/delete/" % (cliente_id, impianto_id, sub_impianto_id)
                return_url = "%s/impianto/%s/" % (cliente_id, impianto_id)

            if detail_type == 'intervento':
                header_msg = '<h1>Attenzione! stai cancellanodo l\'intervento dell\'impianto.</h1>'
                action = '\"Cancella Intervento\"'
                post_url = "%s/impianto/%s/intervento/%s/delete/" % (cliente_id, impianto_id, sub_impianto_id)
                return_url = "%s/impianto/%s/" % (cliente_id, impianto_id)

        data += view_record(cliente_id, detail_type, impianto_id, sub_impianto_id)

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
    search_string = ""
    data_to_render = []
    data = scripts.HOME_ADD_JS
    group_field = ""
    field_order = ""

    if request.method == 'GET' and request.GET != {}:
            form = myforms.FullTextSearchForm(request.GET)
            if form.is_valid():
                    search_string = form.cleaned_data['s']
                    group_field = form.cleaned_data['group_field']
                    field_order = form.cleaned_data['field_order']

            data_to_render = database_manager.search_fullText(search_string, group_field, field_order)
            dr = data_render.DataRender(data_to_render)
            dr.selectColums(cfg.ANAGRAFE_STD_VIEW)

            dr.msgItemsEmpty("<br><h3>La ricerca non ha prodotto risultati.</h3>")
            if search_string != "":
                dr.msgStatistics(("<br><h2>\"%s\" trovati:" % search_string) + " %s</h2><br>")
            dr.showStatistics()
            dr.orderUrl('anagrafe', search_string, group_field, field_order)
            data += dr.toTable()

    return render(request, 'anagrafe.sub', {'query_path':request.get_full_path(), 'data': data,'data_form': form})

import csv
import datetime

def home(request):
    form = myforms.RangeDataSelect()
    data = scripts.HOME_ADD_JS

    # Use default at first time when the home page is never loaded
    search_in_range = ""
    filter_type = None
    ref_month = None
    ref_year = None
    group_field = ""
    field_order = ""

    if request.method == 'GET' and request.GET != {}:
        form = myforms.RangeDataSelect(request.GET)
        if form.is_valid():
            search_in_range = form.cleaned_data['search_in_range']
            filter_type = form.cleaned_data['filter_type']
            ref_month = form.cleaned_data['ref_month']
            ref_year = form.cleaned_data['ref_year']
            group_field = form.cleaned_data['group_field']
            field_order = form.cleaned_data['field_order']

    data_to_render = database_manager.search_inMonth(key=search_in_range,
                                month=ref_month, year=ref_year, filter=filter_type,
                                group_field=group_field, field_order=field_order)
    dr = data_render.DataRender(data_to_render)
    dr.selectColums(cfg.HOME_STD_VIEW)
    dr.urlBar('cliente', ['edit', 'delete'])
    dr.msgItemsEmpty("<br><h3>La ricerca non ha prodotto risultati.</h3>")
    dr.msgStatistics(("<br><h2>Nel mese di %s " % myforms.monthStr(ref_month)) + "%s interventi in scadenza.</h2><br>")
    dr.showStatistics()
    dr.orderUrl('home', search_in_range, group_field, field_order)

    data += dr.toTable()
    return render(request, 'home.sub',{'query_path':request.get_full_path(), 'data': data,'data_form': form})


def exportCSV(request, detail_type=None):

    data_table = []
    filename='Elenco'
    if detail_type is None or detail_type == "home":

        search_in_range = request.GET.get('search_in_range', None)
        filter_type = request.GET.get('filter_type', None)
        ref_month = request.GET.get('ref_month', None)
        ref_year = request.GET.get('ref_year', None)
        group_field = request.GET.get('group_field', None)
        field_order = request.GET.get('field_order', None)

        filename = myforms.monthStr(ref_month)

        data_table = database_manager.search_inMonth(key=search_in_range,
                                month=ref_month, year=ref_year, filter=filter_type,
                                group_field=group_field, field_order=field_order)

    elif detail_type == "anagrafe":
        filename='Anagrafe'

        search_string = request.GET.get('s','')
        group_field = request.GET.get('group_field', None)
        field_order = request.GET.get('field_order', None)
        data_table = database_manager.search_fullText(search_string, group_field, field_order)

    # Create the HttpResponse object with the appropriate CSV header.
    response = http.HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_%s.csv"' % (filename, datetime.datetime.today().strftime("%d-%m-%Y_%X"))

    response.write("\xEF\xBB\xBF")
    writer = tools.UnicodeWriter(response, delimiter=';', quotechar='\"')
    writer.writerow(["%s" % j.replace('_', ' ').capitalize() for j in cfg.ANAGRAFE_STD_VIEW])

    for item_dict in data_table:
        l = []
        for i in cfg.ANAGRAFE_STD_VIEW:
            l.append(data_render.formatFields(item_dict, i, default_text=u"-"))

        writer.writerow(l)

    return response


from main import tools

def populatedb(request):
    #data = tools.insert_csv_files(cli_on=False)
    data = tools.load_csv('/home/asterix/gestionale_www/main/elenco2011.csv')
    return _display_ok(request, "DB aggiornato con sucesso\n" + data)

def test(request, search_string):
    form = myforms.FullTextSearchForm()
    data = scripts.HOME_ADD_JS
    data_to_render = database_manager.query_test(search_string)
    print len(data_to_render)
    """
    for i in data_to_render:
        for v,k in i.items():
            print v, " : ", k
    """

    return render(request, 'anagrafe.sub', {'data': data,'forms': form })


