from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=150)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    place = models.CharField(max_length=150)
    body = models.TextField()
    create_date = models.DateTimeField(auto_now_add = True)
    change_date = models.DateTimeField(auto_now = True)
    
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


