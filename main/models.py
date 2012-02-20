from django.db import models

class Cliente(models.Model):
    codice_id = models.IntegerField()
    cognome = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    codice_fiscale = models.CharField(max_length=17)
    via = models.TextField()
    citta = models.TextField()
    numero_telefono = models.CharField(max_length=20)
    marca_caldaia = models.CharField(max_length=100)
    modello_caldaia = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1)
    combustibile = models.CharField(max_length=100)
    data_installazione = models.DateField()
    data_contratto = models.DateField()


    def __unicode__(self):
        return self.nome



class Interventi(models.Model):
    data = models.DateField()
    cliente = models.ForeignKey(Cliente)

    def __unicode__(self):
        return self.data
