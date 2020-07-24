# Register your models here.
from django.contrib import admin
# from work_orders.models import *
from .models import PartModel, SupplierModel, PartSupplierModel, PartCommentModel
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin

# # Register your models here.
# class partsresource(resources.ModelResource):
#
#     class Meta:
#         model = PartModel
# #
# class supplierresource(resources.ModelResource):
#
#     class Meta:
#         model = SupplierModel
#
# class partsupplierresource(resources.ModelResource):
#
#     class Meta:
#         model = PartSupplierModel
#
# class partcommentsresource(resources.ModelResource):
#
#     class Meta:
#         model = PartCommentModel


# class partcommentsdmin(admin.ModelAdmin):
#     list_display = ('timestamp', 'author', 'part', 'comments')
#     readonly_fields = ('timestamp',)
#
# class importparts(ImportExportModelAdmin):
#     resource_class = partsresource

# class jobsresource(resources.ModelResource):
#
#     class Meta:
#         model = Activities

# admin.site.register(PartModel, importparts)
admin.site.register(PartModel)
# admin.site.register(Activities)
admin.site.register(SupplierModel)
admin.site.register(PartSupplierModel)
# admin.site.register(ActivityRequiredParts)
admin.site.register(PartCommentModel)
# admin.site.register(Tasks)
# admin.site.register(TaskRequiredActivities)
# admin.site.register(WorkCentre)