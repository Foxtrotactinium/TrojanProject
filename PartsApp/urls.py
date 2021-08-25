from django.urls import path
from .views import *

urlpatterns = [
    path('', list_parts, name='inventory'),  # URL path for inventory_list view
    path('history', PartHistoryListView.as_view(), name='parts_history'),  # URL path for inventory_list view
    path('addpart/', add_part, name='addpart'),
    path('parts/<int:part_id>/', info_part, name='info_part'),
    path('parts/<int:part_id>/lowstockgroup', low_stock_group, name='lowstockgroup'),
    path('parts/<int:part_id>/print', print_inventory_label, name='printlabel'),
    path('parts/editsupplierpartnumber/<int:pk>', SupplierPartNumberUpdate.as_view(), name='editsupplierpartnumber'),
    path('parts/<int:part_id>/addsupplier', add_supplier_to_part, name='addpartsupplier'),
    path('addsupplier', add_supplier, name='addsupplier'),
    path("suppliers/", list_supplier, name="suppliers"),
    path('suppliers/<int:id>/', info_supplier, name='info_supplier'),
]
