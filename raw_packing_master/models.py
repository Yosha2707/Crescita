from __future__ import unicode_literals
from django.db import models
from mode_master.models import mode



class raw(models.Model):
    
    mode = models.ForeignKey(mode)
    material_type = models.CharField(max_length=100, default=None)
    material_name = models.CharField(max_length=100,  default=None)
    purchase_name = models.CharField(max_length=100,  default=None)
    purchase_date = models.DateField(auto_now_add=True)
    factory_wise_bifercation = models.CharField(max_length=100,  default=None)
    ex_factory_price = models.FloatField(default=0)
    supplier_name = models.CharField(max_length=100,  default=None)
    hsn_code = models.CharField(max_length=100,  default=None)
    price_after_gst=models.IntegerField(default=0)
    gst=models.FloatField(default=0)
    price_after_gst=models.FloatField(default=0)
    transpoter = models.CharField(max_length=100,  default=None)
    freight=models.FloatField(default=0)
    cost_price=models.FloatField(default=0)
   
   



class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
