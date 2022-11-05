from django.db import models

# Create your models here.

class Season(models.Model):
    ORDER_ID = models.CharField(max_length= 30)
    ORDER_DT = models.DateField()
    QT_ORDD = models.IntegerField()

class Customer_Order(models.Model):
    order_number = models.CharField(max_length= 30)
    item_name = models.CharField(max_length= 30)
    status = models.CharField(max_length= 30)

class Detecting_Change(models.Model):
    date = models.DateField()
    was_rainy = models.BooleanField()
