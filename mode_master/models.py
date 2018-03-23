
from django.db import models
from django.forms import ModelForm

class mode(models.Model):
   
    mode_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_by = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modify_by = models.IntegerField(default=0)
    modify_date = models.DateTimeField(auto_now_add=True, blank=True)

class head(models.Model):
    factory = models.FloatField(default=0, null=True, blank=True)


