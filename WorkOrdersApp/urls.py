from django.urls import path
from .views import *


urlpatterns = [
    path('workcentre/', work_centre_list, name='workcentre'),
    path('workcentre/addworkcentre/', add_work, name='addwork'),
    path('workcentre/<str:vehicle>/', work_information, name='workcentretasks'),
    path('workcentre/<str:vehicle>/<str:task>', work_task_information, name='workcentretasksactivities'),
    path('workcentre/<str:vehicle>/<str:task>/<str:activity>', work_task_activity_information, name='workcentretaskactivityparts'),
]