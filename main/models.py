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
		return self.marca_caldaia

class ImpiantoForm(forms.ModelForm):
	class Meta:
		model = Impianto


VERIFICHE_TYPE = (
	('programmata', 'Manutenzione Ordinaria'),
	('straordinaria', 'Manutenzione Straordinaria'),
	('accensione','Prima Accensione'),
	('altro','Altro..'),
	)

BOLLINO_COLOR_CHOICES = (
	('blu','Blu'),
	('verde','Verde'),
	('giallo','Giallo'),
	('arancione','Arancione'),
	('no','No'),
	('altro','Altro..'),
	)

class Verifica(models.Model):
	stato_verifica = models.BooleanField(default=False)
	data_verifica = models.DateField(default=datetime.date.today())
	verifica_impianto = models.ForeignKey(Impianto)
	tipo_verifica = models.CharField(max_length=80, null=True, blank=True, choices=VERIFICHE_TYPE)
	codice_id = models.CharField(max_length=15, null=True, blank=True)
	numero_rapporto = models.CharField(max_length=15, null=True, blank=True)

    # Sezione manutenzione ordinaria/straordinaria
	prossima_verifica = models.DateField(null=True, blank=True)

    # Sezione analisi combustione
	colore_bollino = models.CharField(max_length = 100, null=True, blank=True, choices=BOLLINO_COLOR_CHOICES)
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
	class Meta:
		model = Verifica

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

"""
BOLLINO_COLOR_CHOICES = (
	('Blu','Blu'),
	('Verde','Verde'),
	('Giallo','Giallo'),
	('Arancione','Arancione'),
	('No','No'),
	)
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
