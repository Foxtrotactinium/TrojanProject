from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(ActivityModel)
admin.site.register(ActivityPartModel)
admin.site.register(TaskModel)
admin.site.register(TaskActivityModel)
