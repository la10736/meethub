from django.db import models
from django.utils import timezone
from events.models import BaseAbstract, Event
from hubs.models import Hub

import logging

class Dispatcher(BaseAbstract):
    name = models.TextField(max_length=60)
    description = models.TextField(max_length=250)
    events = models.ManyToManyField(Event, through='EventDispatched')
    
    hub = models.ForeignKey(Hub, null=True)

    def _event_dispatched(self, ev):
        logging.info("Event %s dispatched by %s"%(ev.title,self.name))
        EventDispatched.objects.create(dispatcher=self, event=ev,
                                            when=timezone.now())
    
    def dispatch(self, ev):
        d = self.cast().dispatch
        if self.dispatch == d:
            raise NotImplementedError("Override this method in the real class")
        d(ev)
    
    def update(self, ev):
        u = self.cast().update
        if self.update == u:
            logging.debug("Standard update implementation: use dispatch for %s"%(str(ev)))
            self.dispatch(ev)
        else:
            u(ev)

class EventDispatched(models.Model):
    event = models.ForeignKey(Event)
    dispatcher = models.ForeignKey(Dispatcher)
    when = models.DateField()

class DebugDispatcher(Dispatcher):
    cls_tag = "dbg"
    tag = models.TextField(max_length=60)
    
    def dispatch(self, ev):
        logging.info("Dispatching %s"%(str(ev)))
        self._event_dispatched(ev)

    def update(self, ev):
        logging.info("Update %s"%(str(ev)))

class TestDispatcher(Dispatcher):
    cls_tag = "tst"
    test = models.TextField(max_length=25)

    def dispatch(self, ev):
        logging.info("TEST Dispatching %s"%(str(ev)))
        self._event_dispatched(ev)

    def update(self, ev):
        logging.info("Update %s"%(str(ev)))    