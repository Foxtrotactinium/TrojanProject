from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register, name="register"),
    path("logout/", logout_request, name="logout"),
    path("login/", login_request, name="login"),
]
