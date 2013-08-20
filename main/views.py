#!/usr/bin/env python
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
            return generate_report2(request, data_to_render)
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
            "<input class=\"btn btn-info\" type=\"button\" name=\"button_action\" value=\"Seleziona Tutti\">",
            "<input class=\"btn btn-info\" type=\"submit\" name=\"button_action\" value=\"Lettera\">",
            "<input class=\"btn btn-info\" type=\"submit\" name=\"button_action\" value=\"Apri\">",
            "<input class=\"btn btn-info\" type=\"submit\" name=\"button_action\" value=\"Chiudi\">",
            "<input class=\"btn btn-info\" type=\"submit\" name=\"button_action\" value=\"Sospendi\">",
    ]

    tb_left = [
            "<input type=\"checkbox\" name=\"row_select\" value=\"<cliente_id>,<impianto_id>,<verifica_id>,<intervento_id>\">"
    ]
    dr.toolbar(top=tb_top, left=tb_left)

    dr.msgItemsEmpty("<br><h3>La ricerca non ha prodotto risultati.</h3>")
    dr.msgStatistics(("<br><h2>Nel mese di %s " % myforms.monthStr(form_dict['ref_month'])) + "%s interventi in scadenza.</h2><br>")
    dr.showStatistics()

    dr.orderUrl('home', form_dict)
    data += dr.toTable()

    if d:
       notification = data_render.notification(d['message_hdr'], d['message'], d['message_type'])

    return render(request, 'home.sub',{'query_path':request.get_full_path(),
                                       'notification': notification,
                                       'data': data,
                                       'data_form': form,
                                       'scripts': scripts.HOME_ADD_JS,
                                       })


def exportCSV(request, detail_type=None):
    data_table = []
    filename='Elenco'
    form_dict = {
            'search_keys' : "",
            'filter_type' : None,
            'ref_month' : None,
            'ref_year' : None,
            'order_by_field' : "",
            'ordering' : "",
    }
    if detail_type is None or detail_type == "home":

        form_dict['search_keys'] = request.GET.get('search_keys', None)
        form_dict['filter_type'] = request.GET.get('filter_type', None)
        form_dict['ref_month'] = request.GET.get('ref_month', None)
        form_dict['ref_year'] = request.GET.get('ref_year', None)
        form_dict['order_by_field'] = request.GET.gorder_by_field('order_by_field', None)
        form_dict['ordering'] = request.GET.get('ordering', None)

        filename = myforms.monthStr(form_dict['ref_month'])

        data_table = database_manager.search_inMonth(**form_dict)

    elif detail_type == "anagrafe":
        filename='Anagrafe'

        form_dict['search_keys'] = request.GET.get('search_keys','')
        form_dict['order_by_field'] = request.GET.get('order_by_field', None)
        form_dict['ordering'] = request.GET.get('ordering', None)
        data_table = database_manager.search_fullText(form_dict['search_keys'], form_dict['order_by_field'], form_dict['ordering'])

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

def convert_utf(str):
    return ''.join([c if ord(c) < 128 else u'\\u' + unicode(ord(c)) + u'?' for c in unicode(str)])

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

import subprocess
from django.template import Context, Template

#def check_rst(request):
def generate_report2(request, items, file_name=None):
    #with open(gestionale.local_settings.LOCAL_TEMPLATE_PATH + 'lettera.rtf', 'r') as in_tpl:
    #['rst2pdf', 'manual.txt', '-o', 'uno.pdf', '-s', 'manual.style']
    date_str = datetime.date.today()
    date_str = date_str.strftime(cfg.DATA_FIELD_STR_FORMAT)

    d = tempfile.mkdtemp()
    in_t = open(os.path.join(gestionale.local_settings.LOCAL_TEMPLATE_PATH, 'lettera_template.txt'), 'r')
    in_hdr = open(os.path.join(gestionale.local_settings.LOCAL_TEMPLATE_PATH, 'lettera_hdr.txt'), 'r')
    tpl = in_t.read()
    tpl_hdr = in_hdr.read()
    print subprocess.call(["cp", "%s" % os.path.join(gestionale.local_settings.LOCAL_TEMPLATE_PATH, 'logo_lettera.jpg'),"%s" % d])

    txt = os.path.join(d,"out.txt")
    with open(txt, 'wb') as out_txt:
        out_txt.write(tpl_hdr)
        for i in items:
            i['data'] = date_str
            t = Template(tpl)
            c = Context(i)
            out_txt.write(t.render(c).encode('utf8'))

    outfile = os.path.join(d,"out.pdf")
    print open(txt,'r').read()
    cmd = ["rst2pdf",
            "%s" % txt,
            "-o",
            "%s" % outfile,
            "-s",
            "%s" % os.path.join(gestionale.local_settings.LOCAL_TEMPLATE_PATH, 'lettera_template.style'),
            ]

    try:
        print subprocess.check_call(cmd)
    except (subprocess.CalledProcessError, OSError), m:
        logger.error("Pdf subprocess: %s" % m)
        return errors.server_error(request)

    response = http.HttpResponse(open(outfile, 'r'), mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lettere.pdf"'
    return response

def err(request):
    return errors.server_error(request)

def check_test(request):
    return render(request, 'anagrafe.sub', {'data': "" })

def maps(request):
    data = scripts.MAPS_ADD_JS
    return render(request, 'maps.sub',{'query_path':request.get_full_path(), 'data': data})

def populatedb(request):
    #data = tools.insert_csv_files(cli_on=False)
    data = tools.load_csv('/home/asterix/gestionale_www/main/elenco2011.csv')
    return _display_ok(request, "DB aggiornato con sucesso\n" + data)

def test(request, search_string):
    form = myforms.FullTextSearchForm()
    data = scripts.HOME_ADD_JS
    data_to_render = database_manager.query_test(search_string)
    print len(data_to_render)
    return render(request, 'anagrafe.sub', {'data': data,'forms': form })
