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


YEARS = [ (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989),
        (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999),
        (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009),
        (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019),
        (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029),
        (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039),
        (2040, 2040)]


def monthStr(ref_month):
    if ref_month is None or ref_month == "":
        ref_month = datetime.date.today().month

    return "%s" % dict(MONTH_CHOISE)[str(ref_month)]


class RangeDataSelect(forms.Form):
    search_keys = forms.CharField(label="Cerca tra le scadenze ", required=False, initial='',
            widget=forms.TextInput(attrs={'class':'input-xlarge', 'placeholder':'Cerca tra le scadenze..'}))
    filter_type = forms.CharField(label="Tipo scadenza", initial='all', required=False,
                widget=forms.Select(choices=FILTER_TYPES, attrs={}))
    ref_month = forms.CharField(label="Mese di riferimento", initial=datetime.date.today().month, required=False,
                widget=forms.Select(choices=MONTH_CHOISE, attrs={}))
    ref_year = forms.CharField(label="Anno di riferimento", initial=datetime.date.today().year, required=False,
            widget=forms.Select(choices=YEARS, attrs={}))
    order_by_field = forms.CharField(label="Raggruppa per ", initial='Raggruppa per..', required=False, widget=forms.Select())
    ordering = forms.CharField(label="Ordinamento", initial='A->Z', required=False, widget=forms.Select())

from django import forms
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class CustomRadioSelect(RadioFieldRenderer):
    def render(self):
        s = u"<span>"
        for i in self:
            sub = unicode(i)
            s += sub.replace("<label", "<label class=\"checkbox inline\" ")
        s += u"</>"
        return mark_safe(s)


class UploadFileForm(forms.Form):
    file  = forms.FileField(label='Seleziona il file')


