# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


# Inventory Model with fields
class PartModel(models.Model):
    partNumber = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=20)
    stockOnHand = models.IntegerField(blank=True)
    minimumStock = models.IntegerField(blank=True)
    reorderQtys = models.IntegerField(blank=True)
    boxSize = models.IntegerField(blank=True)
    leadtime = models.CharField(max_length=50)
    weight = models.IntegerField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.partNumber


class SupplierModel(models.Model):
    supplierName = models.CharField(max_length=50)
    phoneNumber = models.IntegerField(blank=True)
    address = models.CharField(max_length=200)
    accountNumber = models.CharField(max_length=50)

    def __str__(self):
        return self.supplierName


# lookup for many to many relationship between parts and Suppliers
class PartSupplierModel(models.Model):
    supplierPartNumber = models.CharField(max_length=50)
    supplier = models.ForeignKey(SupplierModel, on_delete=models.CASCADE)
    part = models.ForeignKey(PartModel, on_delete=models.CASCADE)
    preferred = models.BooleanField(default=False)

    def setPreferred(self):

        supp_list = PartSupplierModel.objects.all().filter(part=self.part)

        for supp in supp_list:
            supp.preferred = False
            supp.save()

        self.preferred = True
        self.save()


    def __str__(self):
        return str(self.supplier) + " - " + str(self.supplierPartNumber)


class PartCommentModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    part = models.ForeignKey(PartModel, on_delete=models.PROTECT)
    comment = models.TextField()

    def __str__(self):
        return str(self.timestamp.strftime("%d/%m/%Y")) + " - " + str(self.author) + " - " + str(self.comment)
