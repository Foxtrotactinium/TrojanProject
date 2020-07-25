from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from ActivitiesApp.models import TaskModel, ActivityModel
from PartsApp.models import PartModel


class WorkCentreModel(models.Model):
    vehicle = models.CharField(max_length=50)
    task = models.ForeignKey(TaskModel, on_delete=models.PROTECT)
    activity = models.ForeignKey(ActivityModel, on_delete=models.PROTECT)
    part = models.ForeignKey(PartModel, on_delete=models.PROTECT)
    increment = models.BooleanField(default=False)
    quantityRequired = models.IntegerField()
    quantityCompleted = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
