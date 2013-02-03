from django import forms

import datetime
import calendar
import logging
logger = logging.getLogger(__name__)

FILTER_FIELD = (
    ("main_cliente.cognome", "Cognome.."),
    ("main_cliente.nome", "Nome.."),
    ("main_cliente.via", "Via.."),
    ("main_cliente.citta", "Citta.."),
    ("main_impianto.marca_caldaia", "Marca Caldaia.."),
    ("main_impianto.modello_caldaia", "Modello Caldaia.."),
    ("main_impianto.combustibile", "Combustibile.."),
    ("main_impianto.data_installazione", "Data Installazione.."),
    ("main_impianto.data_contratto", "Data Contratto.."),
    ("main_impianto.potenza_caldaia", "Potenza Caldaia.."),
    ("main_impianto.tipo_caldaia", "Tipo Caldaia.."),
        )
FILTER_ORDER = (
        ('ASC', 'A->Z'),
        ('DESC', 'Z->A'),
        )

class FullTextSearchForm(forms.Form):
    s = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size':'40'}))
    group_field = forms.CharField(label="Raggruppa per ", initial='Raggruppa per..', required=False, widget=forms.Select(choices=FILTER_FIELD))
    field_order = forms.CharField(label="Ordinamento", initial='A->Z', required=False, widget=forms.Select(choices=FILTER_ORDER))

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


def monthStr(ref_month):
    if ref_month is None or ref_month == "":
        ref_month = datetime.date.today().month

    return "%s" % dict(MONTH_CHOISE)[str(ref_month)]


class RangeDataSelect(forms.Form):
    search_in_range = forms.CharField(label="Cerca tra le scadenze ", required=False, max_length=200, widget=forms.TextInput(attrs={'size':'40'}))
    filter_type = forms.CharField(label="Intervento", initial='all', required=False, widget=forms.Select(choices=FILTER_TYPES))
    ref_month = forms.CharField(label="Mese di riferimento", initial=datetime.date.today().month, required=False, widget=forms.Select(choices=MONTH_CHOISE))
    ref_year = forms.CharField(label="Anno di riferimento", initial=datetime.date.today().year, required=False, max_length=4, widget=forms.TextInput(attrs={'size':'4'}))
    group_field = forms.CharField(label="Raggruppa per ", initial='Raggruppa per..', required=False, widget=forms.Select(choices=FILTER_FIELD))
    field_order = forms.CharField(label="Ordinamento", initial='A->Z', required=False, widget=forms.Select(choices=FILTER_ORDER))

