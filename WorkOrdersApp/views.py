from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils import timezone

from ActivitiesApp.models import TaskActivityModel, ActivityPartModel, ActivityModel
from .forms import work_form
from .models import WorkCentreModel


def work_centre_list(request):
    return render(request, 'templates/workcentre.html', {'header': 'Outstanding Jobs',
                                               'workcentre': WorkCentreModel.objects.values_list('vehicle', flat=True).distinct()})


def add_work(request):
    if request.method == "POST":
        form = work_form(request.POST)
        if form.is_valid():
            vehicle = form.cleaned_data['vehicle']

            if WorkCentreModel.objects.filter(vehicle=vehicle).count() > 0:
                messages.error(request, "Vehicle already exists")
                return redirect('addwork')

            task_name = form.cleaned_data['taskName']
            notes = form.cleaned_data['notes']

            # activity = get_object_or_404(TaskActivityModel, taskName=taskName).activityName

            task_activity_list = TaskActivityModel.objects.filter(task_name=task_name)

            for activity in task_activity_list:

                required_list = ActivityPartModel.objects.filter(activityid=activity.activityName)
                for required in required_list:
                    temp = WorkCentreModel(vehicle=vehicle,
                                           task_name=task_name,
                                           activityid=activity.activityName,
                                           partsrequired=required.part,
                                           increment=required.increment,
                                           quantityrequired=required.quantity,
                                           quantitycompleted=0,
                                           timestamp=timezone.now(),
                                           user=request.user,
                                           complete=False,
                                           notes=notes
                                           )
                    temp.save()

            return redirect('workcentre')
    else:
        form = work_form()
        return render(request, 'addwork.html', {'workform': form})


def work_information(request, vehicle):
    tasks = WorkCentreModel.objects.filter(vehicle=vehicle).filter(complete=False).values_list('task_name__task_name', flat=True).distinct()
    return render(request, 'templates/workcentretasks.html', {'header': 'Outstanding TaskModel',
                                                    'vehicle': vehicle,
                                                    'workcentretasks': tasks})


def work_task_information(request, vehicle, task):
    activities = WorkCentreModel.objects.filter(vehicle=vehicle).filter(complete=False).values_list('activityid__activityid', flat=True).distinct()
    return render(request, 'templates/workcentretasksactivities.html', {'header': 'Kits',
                                                              'taskactivities': activities,
                                                              'vehicle':vehicle,
                                                              'task':task})

def work_task_activity_information(request, vehicle, task, activity):
    needed_activities = get_object_or_404(ActivityModel, activityid=activity)
    parts = WorkCentreModel.objects.filter(vehicle=vehicle).filter(complete=False).filter(
        activityid=needed_activities)
    return render(request, 'templates/workcentretaskactivityparts.html', {'header': 'Kits',
                                                                'vehicle':vehicle,
                                                                'task':task,
                                                                'activity':activity,
                                                                'parts': parts})
