from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from PartsApp.models import *


# Create your models here.
from ActivitiesApp.models import GroupModel, ActivityModel, GroupActivityModel, ActivityPartModel
from PartsApp.models import PartModel


class TaskModel(models.Model):
    taskName = models.CharField(max_length=50)
    fleetNumber = models.CharField(max_length=50)
    group = models.ForeignKey(GroupModel, on_delete=models.PROTECT)
    #
    # def isComplete(self):
    #     completedList = TaskActivityModel.objects.filter(task=self)
    #     completedList = [activity for activity in completedList if not activity.isComplete()]
    #     return len(completedList) == 0

    def userGroupCompleted(self, userGroup):
        completedList = TaskActivityModel.objects.filter(task=self)
        completedList = [activity for activity in completedList if not activity.isComplete()]
        completedList = [activity for activity in completedList if activity.activity.workCenter in userGroup]
        return len(completedList) == 0

    def __str__(self):
        return str(self.taskName) + " - " + str(self.group)

    # def triggerNextGroup(self):
    #     triggers = GroupTriggerModel.objects.filter(completedGroup=self.group)
    #
    #     for groupTrigger in triggers:
    #         groupactivitylist = GroupActivityModel.objects.filter(group=groupTrigger.triggerGroup)
    #
    #         newTaskName = self.taskName + " - " + groupTrigger.triggerGroup.workCenter.wcType
    #         newTask = TaskModel(newTaskName, self.fleetNumber, groupTrigger.triggerGroup)
    #         newTask.save()
    #
    #         for activity in groupactivitylist:
    #             required_list = ActivityPartModel.objects.filter(activity=activity.activity)
    #             for required in required_list:
    #                 temp = TaskPartsModel(task=newTask,
    #                                       part=required.part,
    #                                       quantityRequired=required.quantity,
    #                                       quantityCompleted=0,
    #                                       )
    #                 temp.save()

class TaskActivityModel(models.Model):
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivityModel, on_delete=models.PROTECT)
    startTime = models.DateTimeField(default=timezone.now)
    finishTime = models.DateTimeField(null=True)

    def isComplete(self):
        completedList = TaskPartsModel.objects.filter(activity=self)
        completedList = [part for part in completedList if not part.isComplete()]
        return len(completedList) == 0

    def __str__(self):
        return str(self.activity)


class TaskPartsModel(models.Model):
    activity = models.ForeignKey(TaskActivityModel, on_delete=models.CASCADE, null=True)
    part = models.ForeignKey(PartModel, on_delete=models.PROTECT)
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, null=True)
    increment = models.BooleanField()
    quantityRequired = models.IntegerField()
    quantityCompleted = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    serial = models.CharField(max_length=50, null=True)
    order = models.IntegerField(blank=False)
    extra = models.CharField(max_length=50, null=True)
    history = HistoricalRecords()

    # @property
    def isComplete(self):
        return self.quantityRequired == self.quantityCompleted

    def updateQuantity(self, newval, user):
        self.user = user
        change = newval-self.quantityCompleted
        if change != 0:
            if self.increment:
                self.part.stockOnHand += change
                print(change)
            else:
                self.part.stockOnHand -= change
                print(change)
            self.quantityCompleted = newval
            self.save()

            self.part._change_reason = f'{self.activity}:{change}'
            self.part.save()

            if self.activity.isComplete():
                self.activity.finishTime = timezone.now()
                self.activity.save()

    def __str__(self):
        return str(self.part)
