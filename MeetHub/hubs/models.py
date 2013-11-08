from django.db import models
from dispatchers.models import Dispatcher
#from sources.models import Source


class Hub(models.Model):
    '''Un hub riceve gli eventi e li notifica ai
    dispatcher registrati. Non discrimina sulla
    sorgente, ma semplicemente invia tutti i
    suoi eventi alle destinazioni registrati.
    
    Quindi un hub ha una relazione many2many
    con gli eventi.
    
    Nella pratica un hub ha solo una lista di generatori  di sorgenti
    e una lista di dispatcher. Queste sorgenti hanno la
    stessa implementazione dei dispatcher (plugin e ereditarieta').
    '''
    
    name = models.CharField(max_length=80)
    desc = models.CharField(max_length=250)
        
    def __unicode__(self):
        return self.name
