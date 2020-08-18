from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ActivitiesApp.models import GroupActivityModel, ActivityPartModel, ActivityModel, GroupModel
from .forms import WorkForm
from .models import VehicleModel, VehiclePartsModel
from django.contrib.auth.decorators import login_required


@login_required
def info_job(request):
    # print(VehicleModel.objects.filter(group__workCenter__contains='LC'))
    print(VehicleModel.objects.filter(vehiclepartsmodel__user__exact=request.user))
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
            groupname = form.cleaned_data['group']

            groupactivitylist = GroupActivityModel.objects.filter(group=groupname)

            for activity in groupactivitylist:
                required_list = ActivityPartModel.objects.filter(activity=activity.activity)
                for required in required_list:
                    temp = VehiclePartsModel(vehicle=vehicleMy,
                                             part=required.part,
                                             quantityRequired=required.quantity,
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
    group = vehicle.group
    activities = GroupActivityModel.objects.filter(group=group)
    return render(request, 'infoJobActivities.html', {'header': 'Grouped Activities',
                                                      'job': job,
                                                      'jobactivities': activities})


@login_required
def info_job_parts(request, job, activity_id):
    if request.method == "POST":
        for completed in request.POST:
            try:
                updatedvalue = get_object_or_404(VehiclePartsModel, id=int(completed))
                updatedvalue.updateQuantity(int(request.POST[completed]))
            except ValueError:
                pass
    reqParts = ActivityPartModel.objects.filter(activity=activity_id)
    parts = VehiclePartsModel.objects \
        .filter(vehicle=job) \
        .filter(part_id__in=reqParts.values_list("id"))
    if get_object_or_404(VehicleModel,id=job).group.workCenter.wcType == 'PK':
        return render(request, 'infoJobParts.html', {'header': 'Kits',
                                                     'parts': parts})
