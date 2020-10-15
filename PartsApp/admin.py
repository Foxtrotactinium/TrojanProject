# Register your models here.
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
# from work_orders.models import *
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class partsresource(resources.ModelResource):
    class Meta:
        model = PartModel


class suppliersresource(resources.ModelResource):
    class Meta:
        model = SupplierModel


class partsuppliersresource(resources.ModelResource):
    class Meta:
        model = PartSupplierModel


#
# class partcommentsresource(resources.ModelResource):
#
#     class Meta:
#         model = PartCommentModel


# class partcommentsdmin(admin.ModelAdmin):
#     list_display = ('timestamp', 'author', 'part', 'comments')
#     readonly_fields = ('timestamp',)
#
class importparts(ImportExportModelAdmin):
    resource_class = partsresource


class importsuppliers(ImportExportModelAdmin):
    resource_class = suppliersresource


class importpartsuppliers(ImportExportModelAdmin):
    resource_class = partsuppliersresource


# class jobsresource(resources.ModelResource):
#
#     class Meta:
#         model = ActivityModel

admin.site.register(PartModel, importparts)
# admin.site.register(SimpleHistoryAdmin)
# admin.site.register(ActivityModel)
admin.site.register(SupplierModel, importsuppliers)
admin.site.register(PartSupplierModel, importpartsuppliers)
# admin.site.register(ActivityPartModel)
admin.site.register(PartCommentModel)

admin.site.register(PartImageModel)

admin.site.register(PartModel.history.model)
# admin.site.register(GroupModel)
# admin.site.register(GroupActivityModel)
# admin.site.register(TaskModel)
