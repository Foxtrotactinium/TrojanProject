from django.urls import path
from .views import *

urlpatterns = [
    path('', activity_list, name='activities'),  # URL path for inventory_list view
    path('addactivity/', add_activity, name='addactivity'),
    path('activity/<str:id>/', activity_information, name='activityinformation'),
    path('activity/<str:id>/addrequired', add_required_part_to_activity, {'increment': False}, name='addrequired'),
    path('activity/<str:id>/addproduced', add_required_part_to_activity, {'increment': True}, name='addproduced'),
    path('activity/<str:id>/save-part-ordering', save_new_ordering_parts_of_activity, name='save-part-ordering'),

    path('activity/editpart/<int:pk>', ActivityPartUpdate.as_view(), name='editactivitypart'),

    path('activity/deletepart/<int:pk>', ActivityPartDelete.as_view(), name='deleteactivitypart'),
    # path('workcenters/', work_center, name='workcenters'),
    path('groups/', groups, name='groups'),
    path('groups/addgroup/', add_group, name='addgroup'),
    path('groups/<int:id>/', group_information, name='groupinformation'),
    path('groups/<int:id>/save-activity-ordering', save_new_ordering_activities_of_group, name='save-activity-ordering'),
    path('groups/deletegroupactivity/<int:pk>', GroupActivityDelete.as_view(), name='deletegroupactivity'),

    path('groups/<int:id>/addrequired', add_required_activity_to_group, name='addrequiredactivity'),

]
