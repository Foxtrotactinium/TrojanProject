from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Inventory Model with fields
class PartsList(models.Model):
    partnumber = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=20)
    stockonhand = models.IntegerField(blank=True)
    minimumstock = models.IntegerField(blank=True)
    reorderqtys = models.IntegerField(blank=True)
    boxsize = models.IntegerField(blank=True)
    leadtime = models.CharField(max_length=50)
    weight = models.IntegerField(blank=True)

    def __str__(self):
        return self.partnumber


class Suppliers(models.Model):
    supplier = models.CharField(max_length=50)
    phonenumber = models.IntegerField(blank=True)
    address = models.CharField(max_length=200)
    customeraccountnumber = models.CharField(max_length=50)

    def __str__(self):
        return self.supplier

# lookup for many to many relationship between parts and Suppliers
class PartSuppliers(models.Model):
    partsupplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    partnumber = models.ForeignKey(PartsList, on_delete=models.CASCADE)
    preferred = models.BooleanField(default=False)

    def __str__(self):
        return str(self.partsupplier)

class PartComments(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    part = models.ForeignKey(PartsList, on_delete=models.PROTECT)
    comment = models.TextField()

    def __str__(self):
        return str(self.timestamp.strftime("%d/%m/%Y"))+" - "+str(self.author)+" - "+str(self.comment)