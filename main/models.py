from django.db import models
from django.forms import ModelForm
import datetime


MODELS_EMPTY_STRING="-"

class Cliente(models.Model):
    data_creazione = models.DateField(default=datetime.date.today(), editable=False)
    codice_id = models.CharField(default=MODELS_EMPTY_STRING, max_length=15, null=True, blank=True)
    codice_impianto = models.CharField(default=MODELS_EMPTY_STRING, max_length=15, null=True, blank=True)
    cognome = models.CharField(default="", max_length=100, null=True, blank=True)
    nome = models.CharField(default="", max_length=100, null=True, blank=True)
    codice_fiscale = models.CharField(default=MODELS_EMPTY_STRING, max_length=17, null=True, blank=True)
    via = models.CharField(default=MODELS_EMPTY_STRING, max_length=300, null=True, blank=True)
    citta = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    numero_telefono = models.CharField(default=MODELS_EMPTY_STRING, max_length=20, null=True, blank=True)
    numero_cellulare = models.CharField(default=MODELS_EMPTY_STRING, max_length=20, null=True, blank=True)
    mail = models.EmailField(default=MODELS_EMPTY_STRING, null=True, blank=True)
    marca_caldaia = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    modello_caldaia = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    tipo = models.CharField(default=MODELS_EMPTY_STRING, max_length=1, null=True, blank=True)
    combustibile = models.CharField(default=MODELS_EMPTY_STRING, max_length=100, null=True, blank=True)
    data_installazione = models.DateField(null=True, blank=True)
    data_contratto = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['cognome']

    def __unicode__(self):
        return ("%s: %s") % (self.cognome, self.citta)

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente


class Intervento(models.Model):
    data = models.DateField(default=datetime.date.today())
    tipo = models.CharField(default=MODELS_EMPTY_STRING,max_length=80, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    numero_rapporto = models.IntegerField(null=True, blank=True)
    scadenza = models.BooleanField(default=False) # Se l'intervento puo' scadere
    data_scadenza = models.DateField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente)

    class Meta:
        ordering = ['-data'] # Ordina per data in modo decrescente

    def __unicode__(self):
        return ("%s: %s") %  (self.tipo, self.data.__str__())

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
        ordering = ['presente']

    def __unicode__(self):
        return ("%s: %s") %  (self.presente, self.data.__str__())
