from django.urls import path
from .views import *


urlpatterns = [
    path('tasks/', task_list, name='tasks'),
    path('task/addtask/', add_task, name='addtask'),
    path('task/<int:taskid>/', info_task_activities, name='infotaskactivities'),
    path('task/<int:taskid>/addTaskActivity', TaskActivityCreate.as_view(), name='addtaskactivity'),
    # path('task/addTaskActivity', TaskActivityCreate.as_view(), name='addtaskactivity'),
    path('task/deleteactivity/<int:pk>', TaskActivityDelete.as_view(), name='deletetaskactivity'),

    path('task/<int:taskid>/<int:taskactivityid>', info_task_parts, name='infotaskparts'),
    path('task/<int:taskid>/<int:taskactivityid>/includerequired', info_task_part_include, {'increment': False}, name='includerequiredpart'),
    path('task/<int:taskid>/<int:taskactivityid>/includeproduced', info_task_part_include, {'increment': True}, name='includeproducedpart'),
    path('task/<int:taskid>/<int:taskactivityid>/completetaskactivity', complete_task_activity , name='completetaskactivity'),
    # path('workcentre/<str:job>/<str:group>/<str:activity>', info_task_parts, name='infojobparts'),
    path('task/editpartserial/<int:pk>', TaskPartSerialUpdate.as_view(), name='edittaskpart-serial'),
    path('task/editpartrequired/<int:pk>', TaskPartRequiredUpdate.as_view(), name='edittaskpart-required'),
    path('task/editpartcompleted/<int:pk>', TaskPartCompletedUpdate.as_view(), name='edittaskpart-completed'),
    path('task/deletepart/<int:pk>', TaskPartDelete.as_view(), name='deletetaskpart'),
    # path('task/deletepart/<int:pk>', ActivityPartDelete.as_view(), name='deleteactivitypart'),
]