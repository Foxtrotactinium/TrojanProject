from django.urls import path
from .views import *

urlpatterns = [
    path('', activity_list, name='activities'),  # URL path for inventory_list view
    path('addactivity/', add_activity, name='addactivity'),
    path('activity/<str:id>/', activity_information, name='activityinformation'),
    path('activity/<str:id>/addrequired', add_required_part_to_activity, name='addrequired'),

    path('tasks/', tasks, name='tasks'),
    path('tasks/addtask/', add_task, name='addtask'),
    path('tasks/<str:id>/', task_information, name='taskinformation'),
    path('tasks/<str:id>/addrequired', add_required_activity_to_task, name='addrequiredactivity'),
]
