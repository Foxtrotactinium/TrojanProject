from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords


# Create your models here.
from ActivitiesApp.models import TaskModel, ActivityModel
from PartsApp.models import PartModel


class VehicleModel(models.Model):
    chassisNumber = models.CharField(max_length=50)
    fleetNumber = models.CharField(max_length=50)
    task = models.ForeignKey(TaskModel, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.chassisNumber)+" - "+str(self.fleetNumber)+" - "+str(self.task)


class VehiclePartsModel(models.Model):
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.PROTECT)
    part = models.ForeignKey(PartModel, on_delete=models.PROTECT)
    quantityCompleted = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.part)
