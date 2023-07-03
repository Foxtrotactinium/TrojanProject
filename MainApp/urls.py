from django.urls import path
from .views import *
from InventoryOutput import export_stocktake_csv

urlpatterns = [
    path("register/", register, name="register"),
    path("logout/", logout_request, name="logout"),
    path("login/", login_request, name="login"),
    path("composertest/", composer_test, name="composertest"),
    path("export/", export_stocktake_csv, name='export_stocktake_csv'),
]
