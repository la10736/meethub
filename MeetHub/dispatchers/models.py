from django.db import models
from django.utils import timezone
from events.models import Event
import logging

# Create your models here.
class Dispatcher(models.Model):
    name = models.TextField(max_length=60)
    description = models.TextField(max_length=250)
    events = models.ManyToManyField(Event, through='EventDispatched')
    
    def _event_dispatched(self, ev):
        logging.info("Event %s dispatched by %s"%(ev.name,self.name))
        ed = EventDispatched.objects.create(disptcher=self, event=ev,
                                            when=timezone.now())
        ed.save()
    
    def dispatch(self, ev):
        raise NotImplementedError("Override this method in the real class")
    
    def update(self, ev):
        logging.debug("Standard update implementation: use dispatch for %s"%(str(ev)))
        self.dispatch()

    class Meta:
        abstract = True

class EventDispatched(models.Model):
    event = models.ForeignKey(Event)
    dispatcher = models.ForeignKey(Dispatcher)
    when = models.DateField()

class DebugDispatcher(Dispatcher):
    tag = models.TextField(max_length=60)
    