from django.urls import path
from .views import *

urlpatterns = [
    path('', inventory_list, name='inventory'),  # URL path for inventory_list view
    path('addpart/', add_part, name='addpart'),
    path('parts/<str:id>/', part_information, name='detail'),
    path('addsupplier', add_supplier, name='addsupplier'),
    path("suppliers/", supplier_list, name="suppliers"),
    path('suppliers/<str:id>/', supplier_information, name='supplier_information'),
]
