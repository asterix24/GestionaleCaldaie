#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from main import myforms

import datetime

class Cliente(models.Model):
    """
    Anagrafica del cliente
    """
    cliente_data_inserimento = models.DateField(default=datetime.date.today(), editable=False)
    nome = models.CharField(max_length=100, null=True, blank=True)
    cognome = models.CharField(max_length=100, db_index=True)
    codice_fiscale = models.CharField(max_length=17, null=True, blank=True)
    via = models.CharField(max_length=300, null=True, blank=True)
    citta = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    cap = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    numero_telefono = models.CharField(max_length=20, null=True, blank=True)
    numero_cellulare = models.CharField(max_length=20, null=True, blank=True)
    mail = models.EmailField(default="", null=True, blank=True)

    class Meta:
        ordering = ['cognome', 'nome']
        unique_together = ('cognome', 'nome', 'codice_fiscale', 'citta','via')

    def __unicode__(self):
        return (u"%s, %s: %s - %s" % (self.cognome, self.nome, self.via, self.citta))

class ClienteForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()

        cleaned_data['cliente_id_inserito'] = None

        _nome = cleaned_data.get("nome", '')
        _cognome = cleaned_data.get("cognome", '')
        _codice_fiscale = cleaned_data.get("codice_fiscale", '')
        _via = cleaned_data.get("via", '')
        _citta = cleaned_data.get("citta", '')
        _cap = cleaned_data.get("cap", '')
        _numero_telefono = cleaned_data.get("numero_telefono", '')
        _numero_cellulare = cleaned_data.get("numero_cellulare", '')
        _mail =cleaned_data.get("mail", '')

        cli = Cliente.objects.filter(models.Q(nome__iexact=_nome) &
                               models.Q(cognome__iexact=_cognome) &
                               models.Q(codice_fiscale__iexact=_codice_fiscale) &
                               models.Q(via__iexact=_via) &
                               models.Q(citta__iexact=_citta) &
                               models.Q(cap__iexact=_cap) &
                               models.Q(numero_telefono__iexact=_numero_telefono) &
                               models.Q(numero_cellulare__iexact=_numero_cellulare) &
                               models.Q(mail__iexact=_mail))

        if len(cli) > 0:
            cleaned_data['cliente_id_inserito'] = cli[0].id
            return cleaned_data

        if _nome is not None:
            cleaned_data['nome'] = _nome.capitalize()
        if _cognome is not None:
            cleaned_data['cognome'] = _cognome.capitalize()
        if _codice_fiscale is not None:
            cleaned_data['codice_fiscale'] = _codice_fiscale.upper()
        if _via is not None:
            cleaned_data['via'] = _via.capitalize()
        if _citta is not None:
            cleaned_data['citta'] = _citta.capitalize()

        # Always return the full collection of cleaned data.
        return cleaned_data

    class Meta:
		model = Cliente

POTENZA_CALDAIA = (
    ('C1'   , 'C1: Inferiore a 35 kW'),
    ('C2'   , 'C2: Compresa tra 35 kW e 350 kW'),
    ('C3'   , 'C3: Uguale o superiore a 350 kW'),
    ('altro', 'Altro..'),
)
POTENZA_CALDAIA_DICT = dict(POTENZA_CALDAIA)

TIPO_CALDAIA = (
    ('A'    , 'A: camera aperta senza canna fumaria'),
    ('B'    , 'B: camera aperta con canna fumaria a tiraggio naturale'),
    ('C'    , 'C: camera chiusa con canna fumaria a tiraggio forzato'),
    ('altro', 'Altro..'),
)
TIPO_CALDAIA_DICT =  dict(TIPO_CALDAIA)

STATO_CALDAIA = (
    ('A'  , 'Attivo'),
    ('S' , 'Scaduto'),
    ('D', 'Dismesso'),
)
STATO_CALDAIA_DICT = dict(STATO_CALDAIA)

class Impianto(models.Model):
    impianto_data_inserimento = models.DateField(default=datetime.date.today(), editable=False)
    stato_impianto = models.CharField(default=None, max_length=100, null=True, blank=True, choices=STATO_CALDAIA)
    cliente_impianto = models.ForeignKey(Cliente, db_index=True)
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
    altra_potenza_caldaia = forms.CharField(label='Altro', max_length=100, required=False, widget=forms.TextInput(attrs={'size':'30'}))
    altro_tipo_caldaia = forms.CharField(label='Altro', max_length=100, required=False, widget=forms.TextInput(attrs={'size':'30'}))
    stato_impianto = forms.CharField(label='Stato impianto', initial='A', required=False,
            widget=forms.RadioSelect(choices=STATO_CALDAIA, renderer=myforms.CustomRadioSelect))

    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        _tipo_caldaia = cleaned_data.get("tipo_caldaia")
        _altro_tipo_caldaia = cleaned_data.get("altro_tipo_caldaia")

        _potenza_caldaia = cleaned_data.get("potenza_caldaia")
        _altra_potenza_caldaia = cleaned_data.get("altra_potenza_caldaia")

        if _tipo_caldaia == 'altro':
            if _altro_tipo_caldaia == '':
                self._errors["tipo_caldaia"] = self.error_class(["Specificare un altro tipo di caldaia."])
                cleaned_data["altro_tipo_caldaia"] = _altro_tipo_caldaia.upper()

        if _potenza_caldaia == 'altro':
            if _altra_potenza_caldaia == '':
                self._errors["potenza_caldaia"] = self.error_class(["Specificare un altra potenza caldaia."])
                cleaned_data["altra_potenza_caldaia"] = _altro_potenza_caldaia.upper()

        _codice_impianto = cleaned_data.get("codice_impianto")
        if _codice_impianto is not None:
            cleaned_data['codice_impianto'] = _codice_impianto.upper()

        _marca_caldaia = cleaned_data.get("marca_caldaia")
        if _marca_caldaia is not None:
            cleaned_data['marca_caldaia'] = _marca_caldaia.upper()

        _modello_caldaia = cleaned_data.get("modello_caldaia")
        if _modello_caldaia is not None:
            cleaned_data['modello_caldaia'] = _modello_caldaia.upper()

        _potenza_caladaia = cleaned_data.get("potenza_caladaia")
        if _potenza_caladaia is not None:
            cleaned_data['potenza_caladaia'] = _potenza_caladaia.upper()

        _tipo_caldaia = cleaned_data.get("tipo_caldaia")
        if _tipo_caldaia is not None:
            cleaned_data['tipo_caldaia'] = _tipo_caldaia.upper()

        _combustibile = cleaned_data.get("combustibile")
        if _tipo_caldaia is not None:
            cleaned_data['combustibile'] = _combustibile.capitalize()

        return cleaned_data

    class Meta:
        model = Impianto
        fields = ('cliente_impianto', 'codice_impianto', 'stato_impianto',
        'marca_caldaia', 'modello_caldaia', 'matricola_caldaia',
        'potenza_caldaia', 'altra_potenza_caldaia', 'tipo_caldaia',
        'altro_tipo_caldaia', 'combustibile', 'data_installazione',
        'data_contratto')


VERIFICHE_TYPE_CHOICES = (
    ('programmata'     , 'Manutenzione Ordinaria'),
	('provafumi'       , 'Prova Fumi'),
	('prima_accensione', 'Prima Accensione'),
	('altro'           , 'Altro..'),
)
VERIFICHE_TYPE_CHOICES_DICT = dict(VERIFICHE_TYPE_CHOICES)

BOLLINO_COLOR_CHOICES = (
    ('blu'      ,'Blu'),
	('verde'    ,'Verde'),
	('giallo'   ,'Giallo'),
	('arancione','Arancione'),
	('no'       ,'No'),
	('altro'    ,'Altro..'),
)
BOLLINO_COLOR_CHOICES_DICT = dict(BOLLINO_COLOR_CHOICES)

STATO_VERIFICA = (
    ('A','Aperto'),
    ('C','Chiuso'),
    ('S','Sospeso'),
 )
STATO_VERIFICA_DICT = dict(STATO_VERIFICA)

STATO_PAGAMENTO = (
    ('True','Pagato'),
    ('False','Non Riscosso'),
)
STATO_PAGAMENTO_DICT = dict(STATO_PAGAMENTO)

class Verifica(models.Model):
	verifica_impianto = models.ForeignKey(Impianto, db_index=True)

	stato_verifica = models.CharField(default='A', max_length=80, null=True, blank=True, choices=STATO_VERIFICA)
	data_verifica = models.DateField(default=datetime.date.today(), null=True, blank=True)
	tipo_verifica = models.CharField(max_length=80, null=True, blank=True, choices=VERIFICHE_TYPE_CHOICES)
	altro_tipo_verifica = models.CharField(max_length=80, null=True, blank=True)
	codice_id = models.CharField(max_length=15, null=True, blank=True)
	numero_rapporto = models.CharField(max_length=15, null=True, blank=True)

    # Sezione manutenzione ordinaria/straordinaria
	prossima_verifica = models.DateField(default=datetime.date.today() + datetime.timedelta(days=365), null=True, blank=True)

    # Sezione analisi combustione
	analisi_combustione = models.NullBooleanField(null=True, blank=True)
	colore_bollino = models.CharField(default='blu', max_length = 100, null=True, blank=True, choices=BOLLINO_COLOR_CHOICES)
	altro_colore_bollino = models.CharField(max_length = 100, null=True, blank=True)
	numero_bollino = models.IntegerField(null=True, blank=True)
	valore_bollino = models.DecimalField(max_digits = 10, decimal_places = 2, null=True, blank=True)
	prossima_analisi_combustione = models.DateField(default=datetime.date.today() + datetime.timedelta(days=365*2), null=True, blank=True)

    # Pagamenti
	stato_pagamento = models.NullBooleanField(null=True, blank=True)
	costo_intervento = models.DecimalField(max_digits = 10, decimal_places = 2, null=True, blank=True)

	note_verifica = models.TextField(null=True, blank=True)

	class Meta:
		ordering = ['data_verifica'] # Ordina per data in modo decrescente

	def __unicode__(self):
		return u"%s" % self.data_verifica

class VerificaForm(forms.ModelForm):
    stato_verifica = forms.CharField(label='Stato verifica', initial='A', required=False,
            widget=forms.RadioSelect(choices=STATO_VERIFICA, renderer=myforms.CustomRadioSelect))
    analisi_combustione = forms.BooleanField(initial=False, required=False)
    tipo_verifica = forms.CharField(label='Motivo dell\'intervento', widget=forms.Select(choices=VERIFICHE_TYPE_CHOICES))
    altro_tipo_verifica = forms.CharField(label='Altro', max_length=100, required=False, widget=forms.TextInput())
    altro_colore_bollino = forms.CharField(label='Altro', max_length=100, required=False, widget=forms.TextInput())
    stato_pagamento = forms.BooleanField(label="Stato pagamento", initial=False, required=False,
             widget=forms.RadioSelect(choices=STATO_PAGAMENTO, renderer=myforms.CustomRadioSelect))
    scadenza_verifica_tra = forms.IntegerField(label='Prossima verifica tra mesi', initial="12", required=False)
    scadenza_fumi_tra = forms.IntegerField(label='Prossima analisi combustione tra mesi', initial="24", required=False)

    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        _tipo_verifica = cleaned_data.get("tipo_verifica")
        _altro_tipo_verifica = cleaned_data.get("altro_tipo_verifica")

        _colore_bollino = cleaned_data.get("colore_bollino")
        _altro_colore_bollino = cleaned_data.get("altro_colore_bollino")



        if _colore_bollino == 'altro':
            if _altro_colore_bollino == '':
                # The table row is hide, so when we reply the error it is hide..
                self._errors["colore_bollino"] = self.error_class(["Specificare un altro tipo di Bollino."])
                cleaned_data["altro_colore_bollino"] = _altro_colore_bollino.capitalize()

        if _tipo_verifica == 'altro':
            if _altro_tipo_verifica == '':
                # The table row is hide, so when we reply the error it is hide..
                self._errors["tipo_verifica"] = self.error_class(["Specificare un altro tipo di Manutenzione."])
                cleaned_data["altro_tipo_verifica"] = _altro_tipo_verifica.capitalize()

        if _tipo_verifica == 'provafumi':
            cleaned_data['analisi_combustione'] = True
        else:
            cleaned_data['prossima_analisi_combustione'] = None
            cleaned_data['analisi_combustione'] = False
            cleaned_data['valore_bollino'] = None
            cleaned_data['numero_bollino'] = None
            cleaned_data['colore_bollino'] = None

        return cleaned_data

    class Meta:
        model = Verifica
        fields = ('stato_verifica', 'verifica_impianto', 'tipo_verifica','altro_tipo_verifica',
                  'data_verifica', 'scadenza_verifica_tra','prossima_verifica',
                  'codice_id', 'numero_rapporto','analisi_combustione',
                  'colore_bollino','altro_colore_bollino',
                  'numero_bollino', 'valore_bollino', 'scadenza_fumi_tra',
                  'prossima_analisi_combustione','costo_intervento', 'stato_pagamento',
                  'note_verifica')

INTERVENTO_TYPE_CHOICES = (
    ('Straordinaria'   , 'Straordinaria'),
	('Riparazione'     , 'Riparazione'),
	('Taratura'        , 'Taratura'),
	('Altro'           , 'Altro..'),
)
INTERVENTO_TYPE_CHOICES_DICT = dict(INTERVENTO_TYPE_CHOICES)

class Intervento(models.Model):
    data_intervento = models.DateField(default=datetime.date.today())
    intervento_impianto = models.ForeignKey(Impianto)
    tipo_intervento = models.CharField(max_length=80, null=True, blank=False, choices=INTERVENTO_TYPE_CHOICES)
    note_intervento = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-data_intervento'] # Ordina per data in modo decrescente

    def __unicode__(self):
        return self.tipo_intervento

class InterventoForm(forms.ModelForm):
    tipo_intervento = forms.CharField(label='Motivo dell\'intervento', widget=forms.Select(choices=INTERVENTO_TYPE_CHOICES))
    class Meta:
        model = Intervento

class Settings(models.Model):
    home_view = models.TextField(default='', null=True, blank=True)
    anagrafe_view = models.TextField(default='', null=True, blank=True)
    anagrafe_cliente_view = models.TextField(default='', null=True, blank=True)
    anagrafe_impianto_view = models.TextField(default='', null=True, blank=True)
    anagrafe_verifica_view = models.TextField(default='', null=True, blank=True)
    anagrafe_intervento_view = models.TextField(default='', null=True, blank=True)
    export_table = models.TextField(default='', null=True, blank=True)

    def __unicode__(self):
        return self.home_view

    class Meta:
        ordering = ['-id'] # Ordina per data in modo decrescente

from main import cfg

class SettingsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()

        def __check_s(d, key):
            v = d.get(key,'')
            l = v.split('-')
            h = []
            for i in l:
                if i in cfg.CFG_ALL:
                    h.append(i)
            return "-".join(h)

        for i in cfg.CFG_TABLE:
            cleaned_data[i[0]] = __check_s(cleaned_data, i[0])

        print "clean: ", cleaned_data
        return cleaned_data

    class Meta:
        model = Settings

