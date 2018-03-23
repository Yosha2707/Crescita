
from __future__ import unicode_literals
from django.db import models
import datetime

class profit(models.Model):
    product_code = models.CharField(max_length=100)
    quantity_sold = models.CharField(max_length=100)
    effective_rate = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    pl_sheet = models.CharField(max_length=100)
    start_date =  models.DateTimeField(blank=True, auto_now=True)
    end_date =  models.DateTimeField( blank=True, auto_now=True)




