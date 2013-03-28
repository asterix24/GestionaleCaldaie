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

import logging
logger = logging.getLogger(__name__)

import csv
import datetime

HOME_MENU = [
    ('check' , ['Seleziona Tutti']),
    ('button', ['Apri','Chiudi','Sospendi'])
]

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

    if request.method == 'POST':
        selected_rows = request.POST.getlist('row_select', [])
        action = request.POST.get('button_action', '')
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
    dr.menuWidget(HOME_MENU)
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
    """
    for i in data_to_render:
        for v,k in i.items():
            print v, " : ", k
    """

    return render(request, 'anagrafe.sub', {'data': data,'forms': form })


from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.platypus import Paragraph, Frame

def check_test1(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.rect(3*cm, 4*cm, 15*cm, 23*cm, fill=0, stroke=1)
    ih, iw = p.drawImage("main/static/logo_besalba.jpg", 4.5*cm, 21.5*cm, width=11*cm, anchor='c', preserveAspectRatio=True)
    #print ih/cm, iw/cm
    p.setLineWidth(1.2)
    p.line(3*cm,4*cm,18*cm,4*cm)
    p.line(3*cm,3.9*cm,18*cm,3.9*cm)


    textobject = p.beginText()
    textobject.setTextOrigin(2.9*cm, 4.2*cm)
    textobject.setFont("Helvetica", 7)
    textobject.textLine("Trattamento  dati  personali:  i  dati  sono  trattati  dalla  BESALBA  IMPIANTI  Snc  nel  rispetto  della    normativa  vigente  (D.Lgs.  196/03)  .")
    p.drawText(textobject)

    textobject = p.beginText()
    textobject.setTextOrigin(11.5*cm, 3.5*cm)
    textobject.setFont("Helvetica-Oblique", 9)
    textobject.textLines('''
    Via della Montagna – 87010 Frascineto (CS)
    T. 0981 32214 /C. 328 6149064 - 320 0888958
    P.IVA 01565380787 - e-mail: info@besalba.it
    www.besalba.it -    PEC: besalba@pec.it
    ''')
    p.drawText(textobject)

    textobject = p.beginText()
    textobject.setTextOrigin(3*cm, 3.5*cm)
    textobject.setFont("Helvetica-Oblique", 9)
    textobject.textLines('''
    Impianti termoidraulici – gas – condizionamento
    Panelli solari – manutenzione caldaie
    Caldaie Junkers Bosch – Centro Assistenza Tecnica
    Impianti Fotovoltaici
    ''')
    p.drawText(textobject)



    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

from django.template.loader import get_template
from django.template import *

def check_test1(request):
    template = get_template('lettera.rtf')
    print template.render({'prova':"funziona!!!"})

import re

def check_test(request):
    pat = re.compile('<(\w+)>')
    b = open('main/templates/out.rtf', 'a')

    for i in range(3):
        a = open('main/templates/lettera.rtf', 'r')
        for line in a:
            l = pat.findall(line)
            if l:
                for k in l:
                    line = line.replace(k, "XXXX" + k + str(i))
            b.write(line)
        print i, a.tell()
        a.close()

    b.close()
    response = http.HttpResponse(mimetype='application/rtf')
    return response



