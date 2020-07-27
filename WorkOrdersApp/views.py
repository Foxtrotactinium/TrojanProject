from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ActivitiesApp.models import TaskActivityModel, ActivityPartModel, ActivityModel
from .forms import WorkForm
from .models import WorkCentreModel
from django.contrib.auth.decorators import login_required


@login_required
def add_job(request):
    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data['vehicle']
            if WorkCentreModel.objects.filter(vehicle=job).count() > 0:
                messages.error(request, "Vehicle already exists")
                return redirect('addjob')

            taskname = form.cleaned_data['task']
            taskactivitylist = TaskActivityModel.objects.filter(task=taskname)
            for activity in taskactivitylist:
                required_list = ActivityPartModel.objects.filter(activity=activity.activity)
                for required in required_list:
                    temp = WorkCentreModel(vehicle=job,
                                           task=taskname,
                                           activity=activity.activity,
                                           part=required.part,
                                           increment=required.increment,
                                           quantityRequired=required.quantity,
                                           quantityCompleted=0,
                                           timestamp=timezone.now(),
                                           user=request.user,
                                           )
                    temp.save()

            return redirect('infojobs')
    else:
        form = WorkForm()
        return render(request, 'addJob.html', {'workform': form})

@login_required
def info_job(request):
    return render(request, 'infoJob.html', {'header': 'Outstanding Jobs',
                                            'jobs': WorkCentreModel.objects.values_list('vehicle',
                                                                                        flat=True).distinct()})

@login_required
def info_job_tasks(request, job):
    tasks = WorkCentreModel.objects \
        .filter(vehicle=job) \
        .values_list('task__taskName', flat=True) \
        .distinct()
    return render(request, 'infoJobTasks.html', {'header': 'Outstanding Tasks',
                                                 'job': job,
                                                 'jobtasks': tasks})

@login_required
def info_job_activities(request, job, task):
    activities = WorkCentreModel.objects \
        .filter(vehicle=job) \
        .values_list('activity__activityName', flat=True) \
        .distinct()
    return render(request, 'infoJobActivities.html', {'header': 'Kits',
                                                      'jobactivities': activities,
                                                      'job': job,
                                                      'task': task})

@login_required
def info_job_parts(request, job, task, activity):
    activity = get_object_or_404(ActivityModel, activityName=activity)
    parts = WorkCentreModel.objects \
        .filter(vehicle=job) \
        .filter(activity=activity)
    return render(request, 'infoJobParts.html', {'header': 'Kits',
                                                 'vehicle': job,
                                                 'task': task,
                                                 'activity': activity,
                                                 'parts': parts})
