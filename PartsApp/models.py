# Create your models here.
from django.db import models, transaction
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.utils.html import mark_safe



# Inventory Model with fields
from ActivitiesApp.models import GroupModel


class PartModel(models.Model):
    partNumber = models.CharField(max_length=50, blank=False, unique=True)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=40)
    stockOnHand = models.IntegerField(blank=True)
    minimumStock = models.IntegerField(blank=True)
    reorderQtys = models.IntegerField(blank=True)
    boxSize = models.IntegerField(blank=True)
    leadtime = models.CharField(max_length=50)
    weight = models.IntegerField(blank=True)
    obsolete = models.BooleanField(default=False)
    group = models.ForeignKey("ActivitiesApp.GroupModel", on_delete=models.PROTECT, blank=True, null=True)
    history = HistoricalRecords()

    def getPreferredSupplier(self):
        supplierList = PartSupplierModel.objects.filter(part=self.id, preferred=True)
        if supplierList.count() == 0:
            return None
        return supplierList.first().supplier

    def __str__(self):
        return self.partNumber


class SupplierModel(models.Model):
    supplierName = models.CharField(max_length=50)

    def __str__(self):
        return self.supplierName


# lookup for many to many relationship between parts and Suppliers
class PartSupplierModel(models.Model):
    supplierPartNumber = models.CharField(max_length=50, null=True)
    supplier = models.ForeignKey(SupplierModel, on_delete=models.CASCADE)
    part = models.ForeignKey(PartModel, on_delete=models.CASCADE)
    preferred = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.preferred:
            if PartSupplierModel.objects.filter(part=self.part).count() == 0:
                self.preferred = True
            return super(PartSupplierModel, self).save(*args, **kwargs)
        with transaction.atomic():
            PartSupplierModel.objects.filter(part=self.part, preferred=True) \
                .update(preferred=False)
            return super(PartSupplierModel, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.supplier) + " - " + str(self.supplierPartNumber)


class PartCommentModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    part = models.ForeignKey(PartModel, on_delete=models.PROTECT)
    comment = models.TextField()

    def __str__(self):
        return str(self.timestamp.strftime("%d/%m/%Y")) + " - " + str(self.author) + " - " + str(self.comment)


class PartImageModel(models.Model):
    part = models.ForeignKey(PartModel, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='images/')

    def image_tag(self):
        return mark_safe('<img src="/media/images/%s" width="150" height="150" />' % (self.image))

    image_tag.short_description = 'Image'
