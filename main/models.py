from django.db import models
from django import forms
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
    marca_caldaia = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    modello_caldaia = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    tipo = models.CharField(default=MODELS_EMPTY_STRING, max_length=1, null=True, blank=True)
    combustibile = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    data_installazione = models.DateField(null=True, blank=True)
    data_contratto = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['cognome']

    def __unicode__(self):
        return ("%s, %s: %s") % (self.cognome, self.nome, self.citta)

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente

INTERVENTI_CHOICES = (
    ('ordinaria', 'Manutenzione Ordinaria'),
    ('straordinaria', 'Manutenzione Straordinaria'),
    ('programmata', 'Manutenzione Programmata'),
    ('combustione', 'Verifica combustione'),
    ('none', 'Altro..'),
)

def interventi_choicesExteded(key):
    for k, t in INTERVENTI_CHOICES:
        if k == key:
            return t
    return key

class Intervento(models.Model):
    data = models.DateField(default=datetime.date.today())
    cliente = models.ForeignKey(Cliente)
    tipo = models.CharField(default=MODELS_EMPTY_STRING, max_length=80, null=True, blank=True)
    numero_rapporto = models.CharField(default=MODELS_EMPTY_STRING, max_length=15, null=True, blank=True)
    scadenza = models.BooleanField(default=False) # Se l'intervento puo' scadere
    data_scadenza = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-data'] # Ordina per data in modo decrescente

    def __unicode__(self):
        return ("%s: %s") %  (self.tipo, self.data.__str__())

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

BOLLINO_COLOR_CHOICES = (
    ('Blu','Blu'),
    ('Verde','Verde'),
    ('Giallo','Giallo'),
    ('Arancione','Arancione'),
    ('No','No'),
    )

class Bollino(models.Model):
    presente = models.BooleanField()
    data = models.DateField(default=datetime.date.today(),null=True, blank=True)
    numero_bollino = models.IntegerField(null=True, blank=True)
    colore = models.CharField(default=MODELS_EMPTY_STRING,max_length = 100, null=True, blank=True)
    valore = models.DecimalField(max_digits = 4, decimal_places = 2, null=True, blank=True)
    scadenza = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente)

    class Meta:
        ordering = ['-data']

    def __unicode__(self):
        return ("%s: %s") %  (self.presente, self.data.__str__())

class BollinoForm(forms.ModelForm):
    colore = forms.CharField(widget=forms.Select(choices=BOLLINO_COLOR_CHOICES))
    class Meta:
        model = Bollino
