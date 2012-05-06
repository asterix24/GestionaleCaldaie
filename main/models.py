from django.db import models

class Cliente(models.Model):
    codice_id = models.IntegerField(null=True)
    codice_impianto = models.IntegerField(null=True)
    cognome = models.CharField(max_length=100, null=True)
    nome = models.CharField(max_length=100, null=True)
    codice_fiscale = models.CharField(max_length=17, null=True)
    via = models.CharField(max_length=300, null=True)
    citta = models.CharField(max_length=100, null=True)
    numero_telefono = models.CharField(max_length=20, null=True)
    numero_cellulare = models.CharField(max_length=20, null=True)
    mail = models.EmailField(null=True)
    marca_caldaia = models.CharField(max_length=100, null=True)
    modello_caldaia = models.CharField(max_length=100, null=True)
    tipo = models.CharField(max_length=1, null=True)
    combustibile = models.CharField(max_length=100, null=True)
    data_installazione = models.DateField(null=True)
    data_contratto = models.DateField(null=True)

    class Meta:
        ordering = ['cognome']

    def __unicode__(self):
        return ("%s: %s") % (self.cognome, self.citta)


class Intervento(models.Model):
    data = models.DateField()
    tipo = models.CharField(max_length=80, null=True)
    note = models.TextField(null=True)
    numero_rapporto = models.IntegerField(null=True)
    scadenza = models.BooleanField(default=False) # Se l'intervento puo' scadere
    data_scadenza = models.DateField(null=True)
    cliente = models.ForeignKey(Cliente)

    class Meta:
        ordering = ['-data'] # Ordina per data in modo decrescente
	
    def __unicode__(self):
        return ("%s: %s") %  (self.tipo, self.data.__str__())

class Bollino(models.Model):
    presente = models.BooleanField()
    data = models.DateField(null=True)
    numero_bollino = models.IntegerField(null=True)
    colore = models.CharField(max_length = 100, null=True)
    valore = models.DecimalField(max_digits = 4, decimal_places = 2, null=True)
    scadenza = models.DateField(null=True)
    note = models.TextField(null=True)
    cliente = models.ForeignKey(Cliente)

    class Meta:
        ordering = ['presente']

    def __unicode__(self):
        return ("%s: %s") %  (self.presente, self.data.__str__())
