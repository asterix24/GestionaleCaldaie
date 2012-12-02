#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django import forms

import datetime

class Cliente(models.Model):
    """
    Anagrafica del cliente
    """
    cliente_data_inserimento = models.DateField(default=datetime.date.today(), editable=False)
    cognome = models.CharField(max_length=100)
    nome = models.CharField(max_length=100, null=True, blank=True)
    codice_fiscale = models.CharField(max_length=17, null=True, blank=True)
    via = models.CharField(max_length=300, null=True, blank=True)
    citta = models.CharField(max_length=100, null=True, blank=True)
    numero_telefono = models.CharField(max_length=20, null=True, blank=True)
    numero_cellulare = models.CharField(max_length=20, null=True, blank=True)
    mail = models.EmailField(default="", null=True, blank=True)

    class Meta:
        ordering = ['cognome', 'nome']

    def __unicode__(self):
        return (u"%s, %s: %s - %s" % (self.cognome, self.nome, self.via, self.citta))

class ClienteForm(forms.ModelForm):
	class Meta:
		model = Cliente

POTENZA_CALDAIA = (
('C1', 'C1: Inferiore a 35 kW'),
('C2', 'C2: Compresa tra 35 kW e 350 kW'),
('C3', 'C3: Uguale o superiore a 350 kW'),
('altro', 'Altro..'),
)

TIPO_CALDAIA = (
('A', 'A: camera aperta senza canna fumaria'),
('B', 'B: camera aperta con canna fumaria a tiraggio naturale'),
('C', 'C: camera chiusa con canna fumaria a tiraggio forzato'),
('altro', 'Altro..'),
)

class Impianto(models.Model):
    impianto_data_inserimento = models.DateField(default=datetime.date.today(), editable=False)
    cliente_impianto = models.ForeignKey(Cliente)
    codice_impianto = models.CharField(max_length=100, null=True, blank=True)
    marca_caldaia = models.CharField(max_length=100, null=True, blank=True)
    modello_caldaia = models.CharField(max_length=100, null=True, blank=True)
    matricola_caldaia = models.CharField(max_length=100, null=True, blank=True)
    potenza_caldaia = models.CharField(max_length=100, null=True, blank=True, choices=POTENZA_CALDAIA)
    altra_potenza_caldaia = models.CharField(max_length=100, null=True, blank=True)
    tipo_caldaia = models.CharField(max_length=100, null=True, blank=True, choices=TIPO_CALDAIA)
    altro_tipo_caldaia = models.CharField(max_length=100, null=True, blank=True)
    combustibile = models.CharField(max_length=100, null=True, blank=True)

    data_installazione = models.DateField(null=True, blank=True)
    data_contratto = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['marca_caldaia']
        #unique_together = ('codice_impianto', 'data_installazione')

    def __unicode__(self):
        return (u"[%s] %s: %s-%s" % (self.codice_impianto, self.cliente_impianto, self.marca_caldaia, self.modello_caldaia))

class ImpiantoForm(forms.ModelForm):
    altra_potenza_caldaia = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'size':'30'}))
    altro_tipo_caldaia = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'size':'30'}))

    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        _tipo_caldaia = cleaned_data.get("tipo_caldaia")
        _altro_tipo_caldaia = cleaned_data.get("altro_tipo_caldaia")

        _potenza_caldaia = cleaned_data.get("potenza_caldaia")
        _altra_potenza_caldaia = cleaned_data.get("altra_potenza_caldaia")

        if _tipo_caldaia == 'altro':
            if _altro_tipo_caldaia == '':
                self._errors["tipo_caldaia"] = self.error_class(["Specificare un altro tipo di caldaia."])
                cleaned_data["altro_tipo_caldaia"] = _altro_tipo_caldaia

        if _potenza_caldaia == 'altro':
            if _altra_potenza_caldaia == '':
                self._errors["potenza_caldaia"] = self.error_class(["Specificare un altra potenza caldaia."])
                cleaned_data["altra_potenza_caldaia"] = _altro_potenza_caldaia

        return cleaned_data

    class Meta:
        model = Impianto
        fields = ('cliente_impianto', 'codice_impianto',
        'marca_caldaia', 'modello_caldaia', 'matricola_caldaia',
        'potenza_caldaia', 'altra_potenza_caldaia', 'tipo_caldaia',
        'altro_tipo_caldaia', 'combustibile', 'data_installazione',
        'data_contratto')


VERIFICHE_TYPE_CHOICES = (
	('programmata', 'Manutenzione Ordinaria'),
	('straordinaria', 'Manutenzione Straordinaria'),
	('prima_accensione','Prima Accensione'),
	('altro','Altro..'),
	)

VERIFICHE_TYPE_CHOISES_DICT = {
    VERIFICHE_TYPE_CHOICES[0][0]:VERIFICHE_TYPE_CHOICES[0][1],
    VERIFICHE_TYPE_CHOICES[1][0]:VERIFICHE_TYPE_CHOICES[1][1],
    VERIFICHE_TYPE_CHOICES[2][0]:VERIFICHE_TYPE_CHOICES[2][1],
    VERIFICHE_TYPE_CHOICES[3][0]:VERIFICHE_TYPE_CHOICES[3][1]
    }

BOLLINO_COLOR_CHOICES = (
	('blu','Blu'),
	('verde','Verde'),
	('giallo','Giallo'),
	('arancione','Arancione'),
	('no','No'),
	('altro','Altro..'),
	)

BOLLINO_COLOR_CHOICES_DICT = {
    BOLLINO_COLOR_CHOICES[0][0]:BOLLINO_COLOR_CHOICES[0][1],
    BOLLINO_COLOR_CHOICES[1][0]:BOLLINO_COLOR_CHOICES[1][1],
    BOLLINO_COLOR_CHOICES[2][0]:BOLLINO_COLOR_CHOICES[2][1],
    BOLLINO_COLOR_CHOICES[3][0]:BOLLINO_COLOR_CHOICES[3][1],
    BOLLINO_COLOR_CHOICES[4][0]:BOLLINO_COLOR_CHOICES[4][1],
    BOLLINO_COLOR_CHOICES[5][0]:BOLLINO_COLOR_CHOICES[5][1]
    }

class Verifica(models.Model):
	stato_verifica = models.BooleanField(default=False)
	data_verifica = models.DateField(default=datetime.date.today())
	verifica_impianto = models.ForeignKey(Impianto)
	tipo_verifica = models.CharField(max_length=80, null=True, blank=True, choices=VERIFICHE_TYPE_CHOICES)
	altro_tipo_verifica = models.CharField(max_length=80, null=True, blank=True)
	codice_id = models.CharField(max_length=15, null=True, blank=True)
	numero_rapporto = models.CharField(max_length=15, null=True, blank=True)

    # Sezione manutenzione ordinaria/straordinaria
	prossima_verifica = models.DateField(default=datetime.date.today() + datetime.timedelta(days=365))

    # Sezione analisi combustione
	analisi_combustione = models.BooleanField(default=False)
	colore_bollino = models.CharField(default='blu', max_length = 100, null=True, blank=True, choices=BOLLINO_COLOR_CHOICES)
	altro_colore_bollino = models.CharField(max_length = 100, null=True, blank=True)
	numero_bollino = models.IntegerField(null=True, blank=True)
	valore_bollino = models.DecimalField(max_digits = 4, decimal_places = 2, null=True, blank=True)
	prossima_analisi_combustione = models.DateField(default=datetime.date.today() + datetime.timedelta(days=365*2), null=True, blank=True)

    # Pagamenti
	stato_pagamento = models.BooleanField(default=False)
	costo_intervento = models.DecimalField(max_digits = 4, decimal_places = 2, null=True, blank=True)

	note_verifica = models.TextField(null=True, blank=True)

	class Meta:
		ordering = ['-data_verifica'] # Ordina per data in modo decrescente

	def __unicode__(self):
		return self.tipo_verifica

class VerificaForm(forms.ModelForm):
    stato_verifica = forms.BooleanField(label='Chiudi verifica', required=False)
    tipo_verifica = forms.CharField(label='Motivo dell\'intervento', widget=forms.Select(choices=VERIFICHE_TYPE_CHOICES))
    altro_tipo_verifica = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'size':'30'}))
    scadenza_verifica_tra = forms.IntegerField(label='Prossima verifica tra mesi', initial="12", required=False)
    scadenza_fumi_tra = forms.IntegerField(label='Prossima analisi combustione tra mesi', initial="24", required=False)

    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        _tipo_verifica = cleaned_data.get("tipo_verifica")
        _altro_tipo_verifica = cleaned_data.get("altro_tipo_verifica")

        _colore_bollino = cleaned_data.get("colore_bollino")
        _altro_colore_bollino = cleaned_data.get("altro_colore_bollino")

        if _tipo_verifica == 'altro':
            if _altro_tipo_verifica == '':
                # The table row is hide, so when we reply the error it is hide..
                self._errors["tipo_verifica"] = self.error_class(["Specificare un altro tipo di Manutenzione."])
                cleaned_data["altro_tipo_verifica"] = _altro_tipo_verifica

        if _colore_bollino == 'altro':
            if _altro_colore_bollino == '':
                # The table row is hide, so when we reply the error it is hide..
                self._errors["colore_bollino"] = self.error_class(["Specificare un altro tipo di Bollino."])
                cleaned_data["altro_colore_bollino"] = _altro_colore_bollino

        return cleaned_data

    class Meta:
        model = Verifica
        fields = ('stato_verifica', 'verifica_impianto', 'tipo_verifica',
                  'data_verifica', 'scadenza_verifica_tra','prossima_verifica',
                  'altro_tipo_verifica', 'codice_id',
                  'numero_rapporto', 'analisi_combustione',
                  'colore_bollino','altro_colore_bollino',
                  'numero_bollino', 'valore_bollino', 'scadenza_fumi_tra',
                  'prossima_analisi_combustione','costo_intervento', 'stato_pagamento',
                  'note_verifica')

class Intervento(models.Model):
	data_intervento = models.DateField(default=datetime.date.today())
	intervento_impianto = models.ForeignKey(Impianto)
	tipo_intervento = models.CharField(max_length=80, null=True, blank=True)
	note_intervento = models.TextField(null=True, blank=True)

	class Meta:
		ordering = ['-data_intervento'] # Ordina per data in modo decrescente

	def __unicode__(self):
		return self.tipo_intervento

class InterventoForm(forms.ModelForm):
	class Meta:
		model = Intervento

