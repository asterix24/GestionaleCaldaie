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
    return render(request, 'anagrafe.sub', {'data': data,'forms': form })


from django.http import HttpResponse
from PyRTF import *

def rtf_encode(unistr):
    return ''.join([c if ord(c) < 128 else u'\\u' + unicode(ord(c)) + u'?' for c in unistr])

def check_test(request):
    # 1000 = 1,27cm
    doc     = Document()
    ss      = doc.StyleSheet
    section = Section(paper=StandardPaper.A4)
    doc.Sections.append(section)

    # Text style
    red_txt = TextPS(colour=ss.Colours.Red, font=ss.Fonts.Arial, size=18)
    blue_txt = TextPS(colour=ss.Colours.Blue, font=ss.Fonts.Arial, size=18)
    txt_small = TextPS(font=ss.Fonts.Arial, size=15)
    txt_normal = TextPS(font=ss.Fonts.Arial, size=27)
    txt_normal_bold = TextPS(font=ss.Fonts.Arial, bold=1, size=27)

    # header section
    image = Image('main/static/logo_besalba.jpg', scale=40)
    section.Header.append(Paragraph(image, ParagraphPS().SetAlignment(3)))

    # footer section


    thin_edge  = BorderPS(width=40, style=BorderPS.SINGLE, spacing=50)
    thin_frame  = FramePS(thin_edge)

    p = Paragraph(ss.ParagraphStyles.Normal)
    p.append(Text('Trattamento dati personali: i dati sono trattati dalla BESALBA IMPIANTI Snc nel rispetto della normativa vigente (D.Lgs. 196/03).', txt_small))
    section.Footer.append(p)

    para_props = ParagraphPS(tabs=[TabPropertySet(alignment=TabPropertySet.LEFT, leader=TabPropertySet.HYPHENS, width=5100)])
    p = Paragraph(ss.ParagraphStyles.Normal, para_props, thin_frame)
    p.append(Text('Impianti termoidraulici - gas - condizionamento', red_txt), TAB, Text('Via della Montagna - 87010 Frascineto (CS)', blue_txt))
    p.append(LINE)
    p.append(Text('Panelli solari - manutenzione caldaie', blue_txt), TAB, Text('T. 0981 32214 C. 328 6149064 - 320 0888958', red_txt))
    p.append(LINE)
    p.append(Text('Caldaie Junkers Bosch - Centro Assistenza Tecnica', red_txt), TAB, Text('P.IVA 01565380787 - e-mail: info@besalba.it', blue_txt))
    p.append(LINE)
    p.append(Text('Impianti Fotovoltaici', blue_txt), TAB, Text('www.besalba.it - PEC: besalba@pec.it',red_txt))

    section.Footer.append(p)

    para_props = ParagraphPS(tabs=[TabPropertySet(alignment=TabPropertySet.LEFT, leader=TabPropertySet.HYPHENS, width=5100)])
    p = Paragraph(ss.ParagraphStyles.Normal, para_props)
    #Text('%s', txt_style)

    for i in range(3):

        p.append(TAB, Text('NOME', txt_normal), TAB, Text('COGNOME', txt_normal))
        p.append(TAB, Text('VIA', txt_normal))
        p.append(TAB, Text('CAP', txt_normal), TAB, Text('CITTA', txt_normal))

        p = Paragraph(ss.ParagraphStyles.Heading1)
        p.append(Text('XXXX\u224\'e0X\u232\'e8X\u236\'ecX\u242\'f2X\u249\'f9XXXX', txt_normal_bold))
        section.append(p)

        p = Paragraph( ss.ParagraphStyles.Normal )
        p.append('This document has different headers and footers for the first and then subsequent pages. '
                  'If you insert a page break you should see a different header and footer.')
        section.append(p)

        p = Paragraph(ss.ParagraphStyles.Normal, ParagraphPS().SetPageBreakBefore(True))
        section.append(p)

    response = http.HttpResponse(mimetype='application/rtf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.rtf"'
    DR = Renderer()
    DR.Write(doc, response)
    return response

