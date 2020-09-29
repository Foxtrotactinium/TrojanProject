from PartsApp.models import PartImageModel
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def activity_list(request):
    return render(request, 'ActivitiesApp/listActivities.html', {'header': 'ActivityModel',
                                                   'activities': ActivityModel.objects.all()})


@login_required
def add_activity(request):
    if request.method == "POST":
        form = activity_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('activities')

    else:
        form = activity_form()

        return render(request, 'ActivitiesApp/addActivity.html', {'activityform': form})


@login_required
def activity_information(request, id):
    activity = get_object_or_404(ActivityModel, id=id)

    if request.method == "POST":
        form = activity_form(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return activity_information(request, id)
        # for qty in request.POST[required.pk]:
        #     print(qty)
        #     try:
        #         updatedvalue = get_object_or_404(ActivityPartModel, id=int(completed))
        #         updatedvalue.updateQuantity(int(request.POST[completed])
        #     except ValueError:
        #         pass

    required = ActivityPartModel.objects.filter(activity=id).filter(increment=False)
    for part in required:
        part.thumbnail = PartImageModel.objects.filter(part=part.part).first()
    produced = ActivityPartModel.objects.filter(activity=id).filter(increment=True)
    for part in produced:
        part.thumbnail = PartImageModel.objects.filter(part=part.part).first()

    form = activity_form(instance=activity)
    context = {'activityform': form,
               'activitypartsrequired': required,
               'activitypartsproduced': produced,
               'activity': activity}
    return render(request, 'ActivitiesApp/infoActivity.html', context)


@login_required
def add_required_part_to_activity(request, id, increment):
    activity = get_object_or_404(ActivityModel, id=id)
    activity_parts = ActivityPartModel.objects.filter(activity=id).filter(increment=increment)
    parts = PartModel.objects.all()
    form = required_part_form(initial={'activity': id, 'increment': increment})
    if increment == False:
        header = "Parts Required"
    else:
        header = "Parts Produced"
    context = {'activity': activity,
               'requiredpartform': form,
               'activityrequiredparts': activity_parts,
               'parts': parts,
               'header': header
               }

    if request.method == "POST":
        form = required_part_form(request.POST)

        if form.is_valid():
            form.save()
        return render(request, 'ActivitiesApp/addActivityPart.html', context)

    return render(request, 'ActivitiesApp/addActivityPart.html', context)


@login_required
def groups(request):
    # print(WorkCenterTypes.objects.filter(wcType=type))

    return render(request, 'ActivitiesApp/listGroups.html', {'header': 'GroupModel',
                                               'groups': GroupModel.objects.all()})


@login_required
def add_group(request):
    if request.method == "POST":
        form = group_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('groups')

    else:
        form = group_form()
        return render(request, 'ActivitiesApp/addGroup.html', {'groupform': form})


@login_required
def group_information(request, id):
    group = get_object_or_404(GroupModel, id=id)
    if request.method == "POST":
        form = group_form(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('groups', group.workCenter)

    else:
        form = group_form(instance=group)
        context = {'groupform': form,
                   'groupactivities': GroupActivityModel.objects.filter(group=id),
                   'id': id}
        return render(request, 'ActivitiesApp/infoGroups.html', context)


@login_required
def add_required_activity_to_group(request, id):
    activities = ActivityModel.objects.all()
    group_activities = GroupActivityModel.objects.filter(group=id)
    group = get_object_or_404(GroupModel, id=id)
    if request.method == "POST":
        form = required_activity_form(request.POST)
        if form.is_valid():
            form.save()
        return redirect('groupinformation', id)

    form = required_activity_form(initial={'group': id})
    context = {'requiredactivityform': form,
               'grouprequiredactivity': group_activities,
               'allactivities': activities,
               }
    return render(request, 'ActivitiesApp/addGroupActivity.html', context)

# @login_required
# def work_center(request):
#
#     return render(request, 'listWorkCenters.html', {'header': 'GroupModel',
#                                                     'workcenters': GroupModel.objects.all(),
#                                                     'types': WorkCenterTypes.objects.all()})

# # use for getting all files in instruction model relating to job from ActivityModel model
# some_manual = Manual.objects.get(id=1)
# some_manual_pdfs = some_manual.manualpdf_set.all()
