from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import *

admin.site.register(VehicleModel)
admin.site.register(VehiclePartsModel, SimpleHistoryAdmin)