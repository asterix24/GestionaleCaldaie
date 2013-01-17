from django import forms

class FullTextSearchForm(forms.Form):
    s = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'size':'40'}))

FILTER_TYPES = (
        ('all', 'Tutti..'),
        ('fumi', 'Analisi combustioni'),
        ('verifiche', 'Verifiche'),
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

import datetime
import calendar

class RangeDataSelect(forms.Form):
    search_in_range = forms.CharField(label="Cerca", required=False, max_length=200, widget=forms.TextInput(attrs={'size':'40'}))
    filter_type = forms.CharField(label="Intervento", required=False, widget=forms.Select(choices=FILTER_TYPES))
    ref_month = forms.CharField(label="Mese di riferimento", required=False, widget=forms.Select(choices=MONTH_CHOISE))
    ref_year = forms.CharField(label="Anno di riferimento", required=False, max_length=4, initial=datetime.date.today().year, widget=forms.TextInput(attrs={'size':'4'}))

