from django.urls import path
from .views import *


urlpatterns = [
    path('workcentre/', info_job, name='infojobs'),
    path('workcentre/addjob/', add_job, name='addjob'),
    path('workcentre/<int:job>/', info_job_activities, name='infojobactivities'),
    path('workcentre/<int:job>/<int:activity_id>', info_job_parts, name='infojobparts'),
    # path('workcentre/<str:job>/<str:task>/<str:activity>', info_job_parts, name='infojobparts'),
]