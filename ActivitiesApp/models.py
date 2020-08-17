from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.contrib.postgres.fields import ArrayField
from PartsApp.models import PartModel
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


# Create your models here.
class ActivityModel(models.Model):
    activityName = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.activityName)


class ActivityPartModel(models.Model):
    activity = models.ForeignKey(ActivityModel, on_delete=models.CASCADE)
    part = models.ForeignKey(PartModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    increment = models.BooleanField(default=False)  # TRUE/FALSE used to represent parts ActivityPartModel/produced
    history = HistoricalRecords()

    def __str__(self):
        return str(self.activity) + " - " + str(self.part)


class GroupModel(models.Model):
    groupName = models.CharField(max_length=50)

    class WorkCenterTypes(models.TextChoices):
        PICKING = 'PK', _('Picking')
        LAZERCUTTING = 'LC', _('Lazer Cutting')
        POWDERCOATING = 'PC', _('Powder Coating')
        ZINCCOATING = 'ZN', _('Zinc Coating')
        HEATTREAT = 'HT', _('Heat Treatment & Shot Peening')
        ROTARYSAW = 'RS', _('Brobo Rotary Saw')
        SHAKEOUT = 'SK', _('Shakeout')
        FOLDING = 'FD', _('Sheet Metal Folding')

    workCenter = models.CharField(max_length=2,
                                  choices=WorkCenterTypes.choices)

    def __str__(self):
        return self.groupName


class GroupActivityModel(models.Model):
    group = models.ForeignKey(GroupModel, on_delete=models.PROTECT)
    activity = models.ForeignKey(ActivityModel, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.group) + ' - ' + str(self.activity)

# class instruction(models.Model):
#     job = models.ForeignKey(ActivityModel, on_delete=models.CASCADE)
#     pdf = models.FileField(upload_to='pdf')
