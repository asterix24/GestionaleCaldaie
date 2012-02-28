from django.db import models

class Cliente(models.Model):
    codice_id = models.IntegerField(null=True)
    cognome = models.CharField(max_length=100, null=True)
    nome = models.CharField(max_length=100, null=True)
    codice_fiscale = models.CharField(max_length=17, null=True)
    via = models.TextField()
    citta = models.TextField()
    numero_telefono = models.CharField(max_length=20, null=True)
    marca_caldaia = models.CharField(max_length=100, null=True)
    modello_caldaia = models.CharField(max_length=100, null=True)
    tipo = models.CharField(max_length=1, null=True)
    combustibile = models.CharField(max_length=100, null=True)
    data_installazione = models.DateField(null=True)
    data_contratto = models.DateField(null=True)


    def __unicode__(self):
        return self.nome


class Interventi(models.Model):
    data = models.DateField()
    cliente = models.ForeignKey(Cliente)

    def __unicode__(self):
        return self.data
