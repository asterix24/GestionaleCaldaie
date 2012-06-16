from django.db import models
from django import forms
from django.utils.datastructures import SortedDict

import datetime

@property
def is_elapse(self):
    if self.data_scadenza < datetime.date.today():
        return False
    return True

MODELS_EMPTY_STRING="-"

class Cliente(models.Model):
    data_creazione = models.DateField(default=datetime.date.today(), editable=False)
    codice_id = models.CharField(default=MODELS_EMPTY_STRING, max_length=15, null=True, blank=True)
    codice_impianto = models.CharField(default=MODELS_EMPTY_STRING, max_length=15, null=True, blank=True)
    cognome = models.CharField(default="", max_length=100)
    nome = models.CharField(default="", max_length=100, null=True, blank=True)
    codice_fiscale = models.CharField(default=MODELS_EMPTY_STRING, max_length=17, null=True, blank=True)
    via = models.CharField(default=MODELS_EMPTY_STRING, max_length=300, null=True, blank=True)
    citta = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    numero_telefono = models.CharField(default=MODELS_EMPTY_STRING, max_length=20, null=True, blank=True)
    numero_cellulare = models.CharField(default=MODELS_EMPTY_STRING, max_length=20, null=True, blank=True)
    mail = models.EmailField(default="", null=True, blank=True)

    class Meta:
        ordering = ['cognome']

    def __unicode__(self):
        return ("%s, %s: %s") % (self.cognome, self.nome, self.citta)

    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        fields = []
        for f in self._meta.fields:
            fname = f.name
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_'+fname+'_display'
            if hasattr( self, get_choice):
                value = getattr( self, get_choice)()
            else:
                try :
                    value = getattr(self, fname)
                except User.DoesNotExist:
                    value = None

            # only display fields with values and skip some fields entirely
            if f.editable and value and f.name not in ('id', 'status', 'workshop', 'user', 'complete') :
                fields.append(
                  {
                   'label':f.verbose_name,
                   'name':f.name,
                   'value':value,
                  }
                )
        return fields

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente

class Impianto(models.Model):
    data_creazione = models.DateField(default=datetime.date.today(), editable=False)
    cliente = models.ForeignKey(Cliente)
    marca_caldaia = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    modello_caldaia = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    tipo = models.CharField(default=MODELS_EMPTY_STRING, max_length=1, null=True, blank=True)
    combustibile = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    data_installazione = models.DateField(null=True, blank=True)
    data_analisi_combustione = models.DateField(null=True, blank=True)
    data_contratto = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['marca_caldaia']

    def __unicode__(self):
        return ("%s, %s: %s") % (self.marca_caldaia, self.modello_caldaia)


BOLLINO_COLOR_CHOICES = (
    ('Blu','Blu'),
    ('Verde','Verde'),
    ('Giallo','Giallo'),
    ('Arancione','Arancione'),
    ('No','No'),
    )

INTERVENTI_CHOICES = (
    ('manutenzione ordinaria', 'manutenzione ordinaria'),
    ('manutenzione straordinaria', 'manutenzione straordinaria'),
    ('interventi tecnici', 'interventi tecnici'),
    ('analisi combustione', 'analisi combustione'),
    ('prima accensione','prima accensione'),
    )

class VerificheManutenzione(models.Model):
    data = models.DateField(default=datetime.date.today())
    cliente = models.ForeignKey(Cliente)
    tipo = models.CharField(default=MODELS_EMPTY_STRING, max_length=80, null=True, blank=True)
    numero_rapporto = models.CharField(default=MODELS_EMPTY_STRING, max_length=15, null=True, blank=True)
    colore_bollino = models.CharField(default=MODELS_EMPTY_STRING,max_length = 100, null=True, blank=True)
    numero_bollino = models.IntegerField(null=True, blank=True)
    valore_bollino = models.DecimalField(max_digits = 4, decimal_places = 2, null=True, blank=True)
    scadenza = models.BooleanField(default=False) # Se l'intervento puo' scadere
    data_scadenza = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-data'] # Ordina per data in modo decrescente

    def __unicode__(self):
        return ("%s: %s") %  (self.tipo, self.data.__str__())


class Intervento(models.Model):
    data = models.DateField(default=datetime.date.today())
    cliente = models.ForeignKey(Cliente)
    tipo = models.CharField(default=MODELS_EMPTY_STRING, max_length=80, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-data'] # Ordina per data in modo decrescente

    def __unicode__(self):
        return ("%s: %s") %  (self.tipo, self.data.__str__())



"""
class BollinoForm(forms.ModelForm):
    colore = forms.CharField(widget=forms.Select(choices=BOLLINO_COLOR_CHOICES))
    class Meta:
        model = Bollino

class InterventoForm(forms.ModelForm):
    tipo = forms.CharField(label='Motivo dell\'intevento', widget=forms.Select(choices=INTERVENTI_CHOICES))
    altro = forms.CharField(label='Altro tipo di intervento',max_length=100, required=False)

    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        _tipo = cleaned_data.get("tipo")
        _altro = cleaned_data.get("altro")
        if _tipo == 'none':
            if _altro == '':
                self._errors["altro"] = self.error_class(["Specificare un altro tipo di intervento."])
                del cleaned_data["altro"]

            cleaned_data["tipo"] = _altro

        return cleaned_data

    class Meta:
        model = Intervento
        exclude = ('scadenza')
        fields = ('data', 'cliente', 'tipo', 'altro', 'numero_rapporto', 'data_scadenza', 'note')

"""
