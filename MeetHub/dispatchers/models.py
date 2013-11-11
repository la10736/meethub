from django.db import models
from django.utils import timezone
from events.models import Event
from hubs.models import Hub
from django.contrib.contenttypes.models import ContentType
import logging

# Create your models here.
class Dispatcher(models.Model):
    real_type = models.ForeignKey(ContentType, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
        super(Dispatcher, self).save(*args, **kwargs)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)
    
    name = models.TextField(max_length=60)
    description = models.TextField(max_length=250)
    events = models.ManyToManyField(Event, through='EventDispatched')
    
    hub = models.ForeignKey(Hub)

    def _event_dispatched(self, ev):
        logging.info("Event %s dispatched by %s"%(ev.title,self.name))
        ed = EventDispatched.objects.create(disptcher=self, event=ev,
                                            when=timezone.now())
        ed.save()
    
    def dispatch(self, ev):
        raise NotImplementedError("Override this method in the real class")
    
    def update(self, ev):
        logging.debug("Standard update implementation: use dispatch for %s"%(str(ev)))
        self.dispatch(ev)
    
    @classmethod
    def get_url_name(cls,tag=''):
        return cls.cls_tag + tag

    @classmethod
    def get_detail_url_name(cls):
        return cls.get_url_name('.detail')
    
    def get_obj_detail_url_name(self):
        return self.cast().get_detail_url_name()

    @classmethod
    def get_index_url_name(cls):
        return cls.get_url_name()
    
    def get_obj_index_url_name(self):
        return self.cast().get_index_url_name()
    
    def get_cls_tag(self):
        return self.cast().cls_tag

class EventDispatched(models.Model):
    event = models.ForeignKey(Event)
    dispatcher = models.ForeignKey(Dispatcher)
    when = models.DateField()

class DebugDispatcher(Dispatcher):
    cls_tag = "dbg"
    tag = models.TextField(max_length=60)

class TestDispatcher(Dispatcher):
    cls_tag = "tst"
    test = models.TextField(max_length=25)

    