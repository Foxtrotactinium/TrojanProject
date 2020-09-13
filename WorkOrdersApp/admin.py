from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import *

admin.site.register(TaskModel)
admin.site.register(TaskActivityModel)
admin.site.register(TaskPartsModel, SimpleHistoryAdmin)