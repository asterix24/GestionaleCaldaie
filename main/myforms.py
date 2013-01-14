from django import forms

class FullTextSearchForm(forms.Form):
    s = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'size':'40'}))


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

def MonthDayList(d=None):
    c = calendar.Calendar()
    if d is None:
        d = datetime.date.today()

    l = []
    for i in c.itermonthdates(d.year, d.month):
        l.append(("%s:%s" % (i.weekday(), i.day), "%.2d, %s" % (i.day, DAY_NAME[i.weekday()])))

    return l

class RangeDataSelect(forms.Form):
    search_in_range = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'size':'40'}))
    start_month = forms.CharField(widget=forms.Select(choices=MONTH_CHOISE))
    start_day = forms.CharField(widget=forms.Select(choices=MonthDayList()))
    start_year = forms.CharField(max_length=4, initial="", widget=forms.TextInput(attrs={'size':'4'}))

