from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ActivitiesApp.models import TaskActivityModel, ActivityPartModel, ActivityModel
from .forms import WorkForm
from .models import VehicleModel, VehiclePartsModel
from django.contrib.auth.decorators import login_required


@login_required
def info_job(request):
    return render(request, 'infoJob.html', {'header': 'Outstanding Jobs',
                                            'jobs': VehicleModel.objects.all()})


@login_required
def add_job(request):
    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():

            if VehicleModel.objects.filter(chassisNumber=form.cleaned_data['chassisNumber']).count() > 0:
                messages.error(request, "Vehicle already exists")
                return redirect('addjob')

            vehicleMy = form.save()
            taskname = form.cleaned_data['task']

            taskactivitylist = TaskActivityModel.objects.filter(task=taskname)

            for activity in taskactivitylist:
                required_list = ActivityPartModel.objects.filter(activity=activity.activity)
                for required in required_list:
                    temp = VehiclePartsModel(vehicle=vehicleMy,
                                             part=required.part,
                                             quantityCompleted=0,
                                             )
                    temp.save()

            return redirect('infojobs')
    else:
        form = WorkForm()
        return render(request, 'addJob.html', {'workform': form})


@login_required
def info_job_activities(request, job):
    vehicle = get_object_or_404(VehicleModel, id=job)
    task = vehicle.task
    activities = TaskActivityModel.objects.filter(task=task)
    return render(request, 'infoJobActivities.html', {'header': 'Outstanding Tasks',
                                                      'job': job,
                                                      'jobactivities': activities})


@login_required
def info_job_parts(request, job, activity_id):
    reqParts = ActivityPartModel.objects.filter(activity=activity_id)
    parts = VehiclePartsModel.objects \
        .filter(vehicle=job) \
        .filter(part_id__in=reqParts.values_list("id"))
    return render(request, 'infoJobParts.html', {'header': 'Kits',
                                                 'parts': parts})
