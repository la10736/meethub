from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class BaseAbstract(models.Model):
    real_type = models.ForeignKey(ContentType, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
        super(BaseAbstract, self).save(*args, **kwargs)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)
    
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
    
    class Meta():
        abstract = True


class Event(BaseAbstract):
    cls_tag = "event"
    
    title = models.CharField(max_length=150)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    place = models.CharField(max_length=150)
    body = models.TextField()
    create_date = models.DateTimeField(auto_now_add = True)
    change_date = models.DateTimeField(auto_now = True)
    
    cancelled = models.BooleanField(default=False)
    
    def is_changed(self):
        return self.change_date != self.create_date
    
    def duration(self):
        return self.end_date - self.start_date
    
    def is_past(self):
        return self.end_date < timezone.now()
    
    def is_future(self):
        return self.start_date > timezone.now()
    
    def is_progress(self):
        now = timezone.now()
        return self.start_date < now < self.end_date()
        
    def __unicode__(self):
        return self.title + '@' + self.place + '[%s]'%(str(self.start_date))


