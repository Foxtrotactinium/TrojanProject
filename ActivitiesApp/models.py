from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.contrib.postgres.fields import ArrayField
from PartsApp.models import PartModel
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import Group

# class WorkCenterTypes(models.Model):
#     wcType = models.CharField(max_length=2)
#     description = models.CharField(max_length=50)
#
#     def __str__(self):
#         return f'{self.wcType} - {self.description}'
#
#         # PICKING = 'PK', _('Picking')
#         # LAZERCUTTING = 'LC', _('Lazer Cutting')
#         # POWDERCOATING = 'PC', _('Powder Coating')
#         # ZINCCOATING = 'ZN', _('Zinc Coating')
#         # HEATTREAT = 'HT', _('Heat Treatment & Shot Peening')
#         # ROTARYSAW = 'RS', _('Brobo Rotary Saw')
#         # SHAKEOUT = 'SK', _('Shakeout')
#         # FOLDING = 'FD', _('Sheet Metal Folding')


class ActivityModel(models.Model):
    activityName = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    workCenter = models.ForeignKey(Group, on_delete=models.PROTECT)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.activityName)

    def getStatus(self):
        parts = ActivityPartModel.objects.filter(activity=self,
                                                 increment=False,
                                                 part__stockOnHand__gt=0)

        if parts.count() == 0:
            return "Waiting"

        return "Active"


class ActivityPartModel(models.Model):
    activity = models.ForeignKey(ActivityModel, on_delete=models.CASCADE)
    part = models.ForeignKey(PartModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    increment = models.BooleanField(default=False)  # TRUE/FALSE used to represent parts ActivityPartModel/produced
    order = models.IntegerField(blank=False, default=100_000)
    history = HistoricalRecords()

    def updateQuantity(self, newval):
        self.quantity = newval
        self.save()

    def __str__(self):
        return str(self.activity) + " - " + str(self.part)


class GroupModel(models.Model):
    groupName = models.CharField(max_length=50)

    def __str__(self):
        return self.groupName


class GroupActivityModel(models.Model):
    group = models.ForeignKey(GroupModel, on_delete=models.PROTECT)
    activity = models.ForeignKey(ActivityModel, on_delete=models.PROTECT)
    order = models.IntegerField(blank=False, default=100_000)

    def __str__(self):
        return str(self.group) + ' - ' + str(self.activity)

# class GroupTriggerModel(models.Model):
#     completedGroup = models.ForeignKey(GroupModel, related_name='completed_group', on_delete=models.CASCADE)
#     triggerGroup = models.ForeignKey(GroupModel, related_name='trigger_group', on_delete=models.CASCADE)

# class instruction(models.Model):
#     job = models.ForeignKey(ActivityModel, on_delete=models.CASCADE)
#     pdf = models.FileField(upload_to='pdf')
