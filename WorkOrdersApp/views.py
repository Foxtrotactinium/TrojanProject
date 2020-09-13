from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ActivitiesApp.models import GroupActivityModel, ActivityPartModel, ActivityModel, GroupModel
from .forms import TaskForm
from .models import TaskModel, TaskPartsModel, TaskActivityModel
from django.contrib.auth.decorators import login_required


@login_required
def task_list(request):
    # print(TaskModel.objects.filter(group__workCenter__contains='LC'))
    # print(TaskModel.objects.filter(taskpartsmodel__user__exact=request.user))
    completedList = TaskModel.objects.all()
    completedList = [task for task in completedList if not task.isComplete()]

    return render(request, 'listTasks.html', {'header': 'Outstanding Tasks',
                                              'tasks': completedList})


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():

            if TaskModel.objects.filter(taskName=form.cleaned_data['taskName']).count() > 0:
                messages.error(request, "Task already exists")
                return redirect('addtask')

            taskMy = form.save()
            groupname = form.cleaned_data['group']

            groupactivitylist = GroupActivityModel.objects.filter(group=groupname)

            for groupactivity in groupactivitylist:
                tempactivity = TaskActivityModel(task=taskMy,
                                                 activity=groupactivity.activity)
                tempactivity.save()
                required_list = ActivityPartModel.objects.filter(activity=groupactivity.activity)
                for required in required_list:
                    temp = TaskPartsModel(activity=tempactivity,
                                          part=required.part,
                                          increment= required.increment,
                                          quantityRequired=required.quantity,
                                          quantityCompleted=0,
                                          )
                    temp.save()

            return redirect('tasks')
    else:
        form = TaskForm()
        return render(request, 'addTask.html', {'taskform': form})


@login_required
def info_task_activities(request, taskid):
    task = get_object_or_404(TaskModel, id=taskid)
    print(task)
    activities = TaskActivityModel.objects.filter(task=task)

    if activities.count() == 1:
        activity = activities.first()
        return info_task_parts(request, taskid, activity.id)

    for activity in activities:
        partsRequired = TaskPartsModel.objects.filter(activity=activity)
        # taskPartsRequired = TaskPartsModel.objects \
        #     .filter(task=taskid) \
        #     .filter(part_id__in=partsRequired.values_list("part"))

        completedList = [part for part in partsRequired if not part.isComplete()]

        if len(completedList) > 0:
            activity.status = activity.activity.getStatus()
        else:
            activity.status = "Done"

    return render(request, 'infoTaskActivities.html', {'header': 'Grouped Activities',
                                                       'taskid': taskid,
                                                       'taskactivities': activities})

@login_required
def info_task_parts(request, taskid, activityid):
    if request.method == "POST":
        for completed in request.POST:
            try:
                updatedvalue = get_object_or_404(TaskPartsModel, id=int(completed))
                updatedvalue.updateQuantity(int(request.POST[completed]), request.user)
            except ValueError:
                pass

    taskPartsRequired = ActivityPartModel.objects.filter(activity=activityid) \
        .filter(increment=False)
    # taskPartsRequired = TaskPartsModel.objects \
    #     .filter(task=taskid) \
    #     .filter(part_id__in=partsRequired.values_list("part"))
    taskPartsProduced = ActivityPartModel.objects.filter(activity=activityid) \
        .filter(increment=True)
    # taskPartsProduced = TaskPartsModel.objects \
    #     .filter(task=taskid) \
    #     .filter(part_id__in=partsProduced.values_list("part"))

    if get_object_or_404(ActivityModel, id=taskid).workCenter.wcType == 'PK':
        return render(request, 'infoTaskParts.html', {'header': 'Kits',
                                                      'producedparts': taskPartsProduced,
                                                      'requiredparts': taskPartsRequired})
    elif get_object_or_404(ActivityModel, id=taskid).workCenter.wcType == 'LC':
        return render(request, 'infoTaskLaserCuttingParts.html', {'header': 'Kits',
                                                                  'producedparts': taskPartsProduced,
                                                                  'requiredparts': taskPartsRequired})
    elif get_object_or_404(ActivityModel, id=taskid).workCenter.wcType == 'PC':
        return render(request, 'infoTaskParts.html', {'header': 'Kits',
                                                      'producedparts': taskPartsProduced,
                                                      'requiredparts': taskPartsRequired})
    elif get_object_or_404(ActivityModel, id=taskid).workCenter.wcType == 'ZN':
        return render(request, 'infoTaskParts.html', {'header': 'Kits',
                                                      'producedparts': taskPartsProduced,
                                                      'requiredparts': taskPartsRequired})
    elif get_object_or_404(ActivityModel, id=taskid).workCenter.wcType == 'HT':
        return render(request, 'infoTaskParts.html', {'header': 'Kits',
                                                      'producedparts': taskPartsProduced,
                                                      'requiredparts': taskPartsRequired})
    elif get_object_or_404(ActivityModel, id=taskid).workCenter.wcType == 'RS':
        return render(request, 'infoTaskParts.html', {'header': 'Kits',
                                                      'producedparts': taskPartsProduced,
                                                      'requiredparts': taskPartsRequired})
    elif get_object_or_404(ActivityModel, id=taskid).workCenter.wcType == 'SK':
        return render(request, 'infoTaskParts.html', {'header': 'Kits',
                                                      'producedparts': taskPartsProduced,
                                                      'requiredparts': taskPartsRequired})
    elif get_object_or_404(ActivityModel, id=taskid).workCenter.wcType == 'FD':
        return render(request, 'infoTaskParts.html', {'header': 'Kits',
                                                      'producedparts': taskPartsProduced,
                                                      'requiredparts': taskPartsRequired})
    elif get_object_or_404(ActivityModel, id=taskid).workCenter.wcType == 'OR':
        taskPartsOrdered = TaskPartsModel.objects.filter(task=taskid)
        return render(request, 'infoTaskOrderingParts.html', {'header': 'Ordered',
                                                              'orderedparts': taskPartsOrdered})
