#!/usr/bmport settings
# -*- coding: utf-8 -*-

from django import http
from django.shortcuts import render

from main import models
from main import myforms
from main import cfg
from main import tools
from main import data_render
from main import database_manager
from main import scripts
from main import errors

import logging
logger = logging.getLogger(__name__)

import csv
import datetime

def __getIds(raw_items, item_id):
    l = []
    for k in raw_items:
        ids = k.split(',')
        l.append(ids[item_id])

    return l

import xlwt
def __export_xls(data_table, filename="tabella"):
    # Create the HttpResponse object with the appropriate CSV header.
    response = http.HttpResponse(mimetype='application/ms-excel; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="%s_%s.xls"' % (filename, datetime.datetime.today().strftime("%d-%m-%Y"))

    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Elenco')

    #Add header
    for colum,j in enumerate(cfg.ANAGRAFE_STD_VIEW):
        sheet.write(0, colum, "%s" % j.replace('_', ' ').capitalize())

    #Write table
    for row,i in enumerate(data_table):
        for colum,j in enumerate(cfg.ANAGRAFE_STD_VIEW):
            #we should skip the header row.
            sheet.write(row + 1, colum, data_render.formatFields(i,j, default_text="-"))

    book.save(response)
    return response


def __export_csv(data_table, filename="tabella"):
    # Create the HttpResponse object with the appropriate CSV header.
    response = http.HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s_%s.csv"' % (filename, datetime.datetime.today().strftime("%d-%m-%Y"))

    response.write("\xEF\xBB\xBF")
    writer = tools.UnicodeWriter(response, delimiter=';')
    writer.writerow(["%s" % j.replace('_', ' ').capitalize() for j in cfg.ANAGRAFE_STD_VIEW])

    for item_dict in data_table:
        l = []
        for i in cfg.ANAGRAFE_STD_VIEW:
            l.append(data_render.formatFields(item_dict, i, default_text="-"))

        writer.writerow(l)

    return response

def export_table(request):
    search_string = request.GET.get('search_keys','')
    data_table = database_manager.search_fullText(search_string)
    return __export_xls(data_table, "Anagrafe")


def home(request, d={}):
    form = myforms.RangeDataSelect()
    data = ''
    notification = ''

    # Use default at first time when the home page is never loaded
    form_dict = {
            'search_keys' : "",
            'filter_type' : None,
            'ref_month' : None,
            'ref_year' : None,
            'order_by_field' : "",
            'ordering' : "",
    }

    if request.method == 'POST':
        selected_rows = request.POST.getlist('row_select', [])
        action = request.POST.get('button_action', '')
        if action == 'Lettera':
            ids = __getIds(selected_rows, data_render.CLIENTE_ID)
            data_to_render = database_manager.search_ids('main_cliente.id', ids)
            return generate_report(data_to_render)
        elif action == 'Scarica Tabella':
            ids = __getIds(selected_rows, data_render.CLIENTE_ID)
            data_to_render = database_manager.search_ids('main_cliente.id', ids)
            return __export_xls(data_to_render, "Elenco")
        else:
            for i in selected_rows:
                ids = i.split(',')
                verifica_id = ids[data_render.VERIFICA_ID]
                if verifica_id != 'None':
                    _id = int(verifica_id)
                    if action == 'Apri':
                        models.Verifica.objects.filter(id=_id).update(stato_verifica='A')
                    if action == 'Chiudi':
                        models.Verifica.objects.filter(id=_id).update(stato_verifica='C')
                    if action == 'Sospendi':
                        models.Verifica.objects.filter(id=_id).update(stato_verifica='S')


    if request.method == 'GET' and request.GET != {}:
        form = myforms.RangeDataSelect(request.GET)
        if form.is_valid():
            form_dict['search_keys'] = form.cleaned_data['search_keys']
            form_dict['filter_type'] = form.cleaned_data['filter_type']
            form_dict['ref_month'] = form.cleaned_data['ref_month']
            form_dict['ref_year'] = form.cleaned_data['ref_year']
            form_dict['order_by_field'] = form.cleaned_data['order_by_field']
            form_dict['ordering'] = form.cleaned_data['ordering']

    data_to_render = database_manager.search_inMonth(**form_dict)
    dr = data_render.DataRender(data_to_render)
    dr.selectColums(cfg.HOME_STD_VIEW)

    tb_top = [
            "<button class=\"btn btn-info dropdown-toggle\" data-toggle=\"dropdown\">Seleziona \
            <span class=\"caret\"></span></button> \
            <ul class=\"dropdown-menu\"> \
            <li><a id=\"action\" href=\"#\">Aperti</a></li> \
            <li><a id=\"action\" href=\"#\">Sospesi</a></li> \
            <li><a id=\"action\" href=\"#\">Chiusi</a></li> \
            <li class=\"divider\"></li> \
            <li><a id=\"action\" href=\"#\">Tutti</a></li> \
            <li><a id=\"action\" href=\"#\">Nessuno</a></li> \
            </ul>",
            "<input class=\"btn btn-info\" type=\"submit\" name=\"button_action\" value=\"Apri\">",
            "<input class=\"btn btn-info\" type=\"submit\" name=\"button_action\" value=\"Chiudi\">",
            "<input class=\"btn btn-info\" type=\"submit\" name=\"button_action\" value=\"Sospendi\">",
            "<input class=\"btn btn-info\" type=\"submit\" name=\"button_action\" value=\"Lettera\">",
            "<input class=\"btn btn-info\" type=\"submit\" name=\"button_action\" value=\"Scarica Tabella\">",
    ]

    tb_left = [
            "<input type=\"checkbox\" name=\"row_select\" id=\"{stato_verifica}\" value=\"{cliente_id},{impianto_id},{verifica_id},{intervento_id}\">"
    ]
    dr.toolbar(top=tb_top, left=tb_left)

    dr.msgItemsEmpty("<br><h3>La ricerca non ha prodotto risultati.</h3>")
    dr.msgStatistics(("<br><h2>Nel mese di %s " % myforms.monthStr(form_dict['ref_month'])) + "COUNT interventi in scadenza.</h2><br>")
    dr.showStatistics()

    dr.orderUrl('home', form_dict)
    data += dr.toTable()


    form_dict['status'] = True
    data_to_render = database_manager.search_inMonth(**form_dict)
    dr = data_render.DataRender(data_to_render)
    dr.selectColums(cfg.HOME_STD_VIEW)
    dr.toolbar(top=tb_top, left=tb_left)
    dr.msgItemsEmpty("")
    dr.msgStatistics(("<br><h2>N.COUNT interventi chiusi nel mese di %s" % myforms.monthStr(form_dict['ref_month'])) + ".</h2><br>")
    dr.showStatistics()
    data += dr.toTable()


    if d:
       notification = data_render.notification(d['message_hdr'], d['message'], d['message_type'])

    return render(request, 'home.sub',{'query_path':request.get_full_path(),
                                       'notification': notification,
                                       'data': data,
                                       'data_form': form,
                                       'scripts': scripts.HOME_ADD_JS,
                                       })

def populatedb(request):
    #data = tools.insert_csv_files(cli_on=False)
    data = tools.load_csv('/home/asterix/gestionale_www/main/elenco2011.csv')
    return _display_ok(request, "DB aggiornato con sucesso\n" + data)

def test(request):
    print request.POST.getlist('or', [])
    show = cfg.HOME_STD_VIEW
    hide = ["Vuota"]
    #print show, hide
    return render(request, 'test.sub', {'items_show': show, 'items_hide':hide })


from django.http import HttpResponse
from functools import partial
from main import data_render
import tempfile
import re
import os,sys
import gestionale

def tag_replace(m, item_dict):
    k = m.group()
    field_name = k[1:-1].lower()
    field = data_render.formatFields(item_dict, field_name, default_text="-")
    return ''.join([c if ord(c) < 128 else u'\\u' + unicode(ord(c)) + u'?' for c in unicode(field)])

def generate_report(items, file_name=None):
    block = []
    block_copy = False
    add_page = False
    date_str = datetime.date.today()
    date_str = date_str.strftime(cfg.DATA_FIELD_STR_FORMAT)
    tmp_file = tempfile.NamedTemporaryFile()

    with open(gestionale.local_settings.LOCAL_TEMPLATE_PATH + 'lettera.rtf', 'r') as in_tpl:
        for line in in_tpl:
            #inizio la copia del blocco.
            if '>>START<<' in line:
                print "Start"
                block_copy = True
                continue

            #inizio la copia del blocco.
            if '>>END<<' in line:
                block_copy = False
                add_page = True
                print "End"

            if block_copy and not add_page:
                block.append(line)
            elif add_page:
                for item in items:
                    item['data'] = date_str
                    for s in block:
                        s = re.sub('(<\w+>)', partial(tag_replace, item_dict=item), s)
                        tmp_file.write(s)

                add_page = False
                block_copy = False
            else:
                tmp_file.write(line)

    tmp_file.seek(0)
    response = http.HttpResponse(tmp_file, mimetype='application/rtf')
    response['Content-Disposition'] = 'attachment; filename="lettere.rtf"'

    return response

def err(request):
    return errors.server_error(request)

def check_test(request):
    return render(request, 'anagrafe.sub', {'data': "" })

def check_layout(request):
    return render(request, 'fluid.html', {})

