from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import *


class activityresource(resources.ModelResource):
    class Meta:
        model = ActivityModel


class importactivities(ImportExportModelAdmin):
    resource_class = activityresource

class activitypartsresource(resources.ModelResource):
    class Meta:
        model = ActivityPartModel


class importactivityparts(ImportExportModelAdmin):
    resource_class = activitypartsresource


admin.site.register(ActivityModel, importactivities)
admin.site.register(ActivityPartModel, importactivityparts)
# admin.site.register(ActivityModel, SimpleHistoryAdmin)
# admin.site.register(ActivityPartModel, SimpleHistoryAdmin)
admin.site.register(GroupModel)
admin.site.register(GroupActivityModel)
admin.site.register(WorkCenterTypes)
