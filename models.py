from django.db import models
from datetime import datetime

# http://stackoverflow.com/a/1383402
class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class Quote(models.Model):
    quote = models.TextField()
    by = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(default=datetime.now)
    promoted = models.DateTimeField(blank=True, null=True)
    
    @ClassProperty
    @classmethod
    def latest(cls):
        found = cls.objects.all().order_by("-promoted")[:1]
        
        if len(found) == 0:
            return None
        else:
            return found[0]
        
    def __unicode__(self):
        return self.quote
