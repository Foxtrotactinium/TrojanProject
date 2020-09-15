from django.urls import path
from .views import *


urlpatterns = [
    path('tasks/', task_list, name='tasks'),
    path('task/addtask/', add_task, name='addtask'),
    path('task/<int:taskid>/', info_task_activities, name='infotaskactivities'),
    path('task/<int:taskid>/<int:taskactivityid>', info_task_parts, name='infotaskparts'),
    # path('workcentre/<str:job>/<str:group>/<str:activity>', info_task_parts, name='infojobparts'),
]