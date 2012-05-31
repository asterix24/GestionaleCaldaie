from django import forms

class FullTextSearchForm(forms.Form):
    s = forms.CharField(max_length=200)
    
class SearchCliente(forms.Form):
    codice_id = forms.IntegerField()
    codice_impianto = forms.IntegerField()
    cognome = forms.CharField(max_length=100)
    nome = forms.CharField(max_length=100)
    codice_fiscale = forms.CharField(max_length=17)
    via = forms.CharField(max_length=300)
    citta = forms.CharField(max_length=100)
    numero_telefono = forms.CharField(max_length=20)
    numero_cellulare = forms.CharField(max_length=20)
    mail = forms.EmailField()
    marca_caldaia = forms.CharField(max_length=100)
    modello_caldaia = forms.CharField(max_length=100)
    tipo = forms.CharField(max_length=1)
    combustibile = forms.CharField(max_length=100)
    data_installazione = forms.DateField()
    data_contratto = forms.DateField()
