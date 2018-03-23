from __future__ import unicode_literals
from django.db import models
from raw_packing_master.models import raw
from mode_master.models import head

class cost(models.Model):

    Raw = models.ForeignKey(raw)
    product_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=100)
    factory_name = models.CharField(max_length=100)
    pack_size = models.CharField(max_length=100)
    rt_id = models.IntegerField(default=0)
    rawmultiplier = models.FloatField(default=0)
    wastage = models.FloatField(default=0)
    overall_wastage = models.FloatField(default=0)
    margin_per= models.FloatField(default=0)
    margin_amount=models.FloatField(default=0)
    mrp_per=models.FloatField(default=0)
    mrp_price=models.FloatField(default=0)
    

   
class costpack(models.Model):
   
    Raw = models.ForeignKey(raw)
    cost = models.ForeignKey(cost)
    packing_id = models.IntegerField(default=0)
    multipliar = models.FloatField(default=0)
    last_updated_on = models.DateTimeField(auto_now_add=True, blank=True)
    