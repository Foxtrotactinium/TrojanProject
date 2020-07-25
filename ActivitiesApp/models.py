from django.db import models
# from django.contrib.postgres.fields import ArrayField
from PartsApp.models import PartModel
from django.contrib.auth.models import User


# Create your models here.
class ActivityModel(models.Model):
    activityName = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.activityName)


class ActivityPartModel(models.Model):
    activity = models.ForeignKey(ActivityModel, on_delete=models.CASCADE)
    # part = models.ForeignKey(PartModel, related_name='required_for_jobs', on_delete=models.CASCADE)
    part = models.ForeignKey(PartModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    increment = models.BooleanField(default=False)  # TRUE/FALSE used to represent parts ActivityPartModel/produced

    def __str__(self):
        return str(self.activity) + " - " + str(self.part)


class TaskModel(models.Model):
    taskName = models.CharField(max_length=50)

    def __str__(self):
        return self.taskName


class TaskActivityModel(models.Model):
    task = models.ForeignKey(TaskModel, on_delete=models.PROTECT)
    activity = models.ForeignKey(ActivityModel, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.task) + ' - ' + str(self.activity)


# class instruction(models.Model):
#     job = models.ForeignKey(ActivityModel, on_delete=models.CASCADE)
#     pdf = models.FileField(upload_to='pdf')
