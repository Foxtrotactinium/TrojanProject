from django.conf.urls import url
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    ]