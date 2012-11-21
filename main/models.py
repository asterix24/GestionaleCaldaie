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
		#unique_together = ('cognome', 'nome')

	def __unicode__(self):
		return self.cognome

class ClienteForm(forms.ModelForm):
	class Meta:
		model = Cliente

POTENZA_CALDAIA = (
('C1', 'C1: Inferiore a 35 kW'),
('C2', 'C2: Compresa tra 35 kW e 350 kW'),
('C3', 'C3: Uguale o superiore a 350 kW'),
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
    codice_impianto = models.CharField(max_length=15, null=True, blank=True)
    marca_caldaia = models.CharField(max_length=100, null=True, blank=True)
    modello_caldaia = models.CharField(max_length=100, null=True, blank=True)
    matricola_caldaia = models.CharField(max_length=100, null=True, blank=True)
    potenza_caldaia = models.CharField(max_length=100, null=True, blank=True, choices=POTENZA_CALDAIA)
    tipo_caldaia = models.CharField(max_length=1, null=True, blank=True, choices=TIPO_CALDAIA)
    combustibile = models.CharField(max_length=100, null=True, blank=True)

    data_installazione = models.DateField(null=True, blank=True)
    data_contratto = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['marca_caldaia']
        #unique_together = ('codice_impianto', 'data_installazione')

    def __unicode__(self):
        return (u"[%s] %s: %s-%s" % (self.codice_impianto, self.cliente_impianto, self.marca_caldaia, self.modello_caldaia))

class ImpiantoForm(forms.ModelForm):
	class Meta:
		model = Impianto


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
	prossima_verifica = models.DateField(null=True, blank=True)

    # Sezione analisi combustione
	analisi_combustione = models.BooleanField(default=False)
	colore_bollino = models.CharField(max_length = 100, null=True, blank=True, choices=BOLLINO_COLOR_CHOICES)
	altro_colore_bollino = models.CharField(max_length = 100, null=True, blank=True)
	numero_bollino = models.IntegerField(null=True, blank=True)
	valore_bollino = models.DecimalField(max_digits = 4, decimal_places = 2, null=True, blank=True)
	prossima_analisi_combustione = models.DateField(null=True, blank=True)

    # Pagamenti
	stato_pagamento = models.BooleanField(default=False)
	costo_intervento = models.DecimalField(max_digits = 4, decimal_places = 2, null=True, blank=True)

	note_verifica = models.TextField(null=True, blank=True)

	class Meta:
		ordering = ['-data_verifica'] # Ordina per data in modo decrescente

	def __unicode__(self):
		return self.tipo_verifica

class VerificaForm(forms.ModelForm):
    stato_verifica = forms.BooleanField(label='Chiudi verifica')
    tipo_verifica = forms.CharField(label='Motivo dell\'intervento', widget=forms.Select(choices=VERIFICHE_TYPE_CHOICES))
    altro_tipo_verifica = forms.CharField(label='', max_length=100,
    required=False, widget=forms.TextInput(attrs={'size':'30'}))
    scadenza_tra = forms.IntegerField(label='Vefica fumi tra mesi', required=False)

    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        _tipo = cleaned_data.get("tipo_verifica")
        _altro = cleaned_data.get("altro_tipo_verifica")
        if _tipo == 'altro':
            if _altro == '':
                # The table row is hide, so when we reply the error it is hide..
                self._errors["tipo_verifica"] = self.error_class(["Specificare un altro tipo di manutenzione."])

                cleaned_data["altro_tipo_verifica"] = _altro

        return cleaned_data

    class Meta:
        model = Verifica
        fields = ('stato_verifica', 'verifica_impianto', 'tipo_verifica',
                  'data_verifica', 'prossima_verifica',
                  'altro_tipo_verifica', 'codice_id',
                  'numero_rapporto', 'analisi_combustione',
                  'scadenza_tra','colore_bollino',
                  'numero_bollino', 'valore_bollino',
                  'costo_intervento', 'stato_pagamento',
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

