from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ActivitiesApp.models import TaskActivityModel, ActivityPartModel, ActivityModel
from .forms import WorkForm
from .models import VehicleModel
from django.contrib.auth.decorators import login_required


@login_required
def add_job(request):
    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data['chassisNumber']
            if VehicleModel.objects.filter(chassisNumber=job).count() > 0:
                messages.error(request, "Vehicle already exists")
                return redirect('addjob')

            taskname = form.cleaned_data['task']
            taskactivitylist = TaskActivityModel.objects.filter(task=taskname)
            for activity in taskactivitylist:
                required_list = ActivityPartModel.objects.filter(activity=activity.activity)
                for required in required_list:
                    temp = VehicleModel(chassisNumber=job,
                                        task=taskname,
                                        part=required.part,
                                        quantityCompleted=0,
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
                                            'jobs': VehicleModel.objects.values_list('chassisNumber',
                                                                                     flat=True).distinct()})

@login_required
def info_job_tasks(request, job):
    tasks = VehicleModel.objects \
        .filter(vehicle=job) \
        .values_list('task__taskName', flat=True) \
        .distinct()
    return render(request, 'infoJobTasks.html', {'header': 'Outstanding Tasks',
                                                 'job': job,
                                                 'jobtasks': tasks})

@login_required
def info_job_activities(request, job, task):
    activities = VehicleModel.objects \
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
    parts = VehicleModel.objects \
        .filter(vehicle=job) \
        .filter(activity=activity)
    return render(request, 'infoJobParts.html', {'header': 'Kits',
                                                 'vehicle': job,
                                                 'task': task,
                                                 'activity': activity,
                                                 'parts': parts})
