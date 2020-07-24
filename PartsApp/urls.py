from django.urls import path
from .views import *

urlpatterns = [
    path('', list_parts, name='inventory'),  # URL path for inventory_list view
    path('addpart/', add_part, name='addpart'),
    path('parts/<str:part_id>/', info_part, name='info_part'),
    path('addsupplier', add_supplier, name='addsupplier'),
    path("suppliers/", list_supplier, name="suppliers"),
    path('suppliers/<str:id>/', info_supplier, name='info_supplier'),
]
