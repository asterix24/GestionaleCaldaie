from django import forms

import datetime
import calendar
import logging
logger = logging.getLogger(__name__)


class FullTextSearchForm(forms.Form):
    search_keys = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size':'40'}))
    order_by_field = forms.CharField(label="Raggruppa per ", initial='Raggruppa per..', required=False, widget=forms.Select())
    ordering = forms.CharField(label="Ordinamento", initial='A->Z', required=False, widget=forms.Select())

FILTER_TYPES = (
       ('all','Tutti..'),
       ('fumi','Analisi combustioni'),
       ('fumi_prossimi','Prossime Analisi combustioni'),
       ('verifiche','Verifiche'),
       ('verifiche_prossima','Prossime Verifiche'),
)

MONTH_CHOISE = (
	('1','Gennaio'),
    ('2','Febbraio'),
	('3','Marzo'),
	('4','Aprile'),
	('5','Maggio'),
	('6','Giugno'),
	('7','Luglio'),
	('8','Agosto'),
	('9','Settembre'),
	('10','Ottobre'),
	('11','Novembre'),
	('12','Dicembre'),
	)

DAY_NAME = {
    0:'Lunedi',
    1:'Martedi',
    2:'Mercoledi',
    3:'Giovedi',
    4:'Venerdi',
    5:'Sabato',
    6:'Domenica',
    }


def monthStr(ref_month):
    if ref_month is None or ref_month == "":
        ref_month = datetime.date.today().month

    return "%s" % dict(MONTH_CHOISE)[str(ref_month)]


class RangeDataSelect(forms.Form):
    search_keys = forms.CharField(label="Cerca tra le scadenze ", required=False, max_length=200,
            widget=forms.TextInput(attrs={'class':'span5', 'placeholder':'Cerca tra le scadenze..'}))
    filter_type = forms.CharField(label="Tipo scadenza", initial='all', required=False,
                widget=forms.Select(choices=FILTER_TYPES))
    ref_month = forms.CharField(label="Mese di riferimento", initial=datetime.date.today().month, required=False,
                widget=forms.Select(choices=MONTH_CHOISE))
    ref_year = forms.CharField(label="Anno di riferimento", initial=datetime.date.today().year, required=False, max_length=4,
            widget=forms.TextInput(attrs={'class':'span1'}))
    order_by_field = forms.CharField(label="Raggruppa per ", initial='Raggruppa per..', required=False, widget=forms.Select())
    ordering = forms.CharField(label="Ordinamento", initial='A->Z', required=False, widget=forms.Select())

from django import forms
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class CustomRadioSelect(RadioFieldRenderer):
    def render(self):
        s = u"<div id=\"radio_fmt\">"
        for i in self:
            s += u"%s<label for=\"id_%s_%s\">%s</label>" % (i.tag(), i.name, i.index, i.choice_label)
        s += u"</div>"
        return mark_safe(s)

