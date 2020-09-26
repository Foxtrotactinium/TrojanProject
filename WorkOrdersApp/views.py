from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ActivitiesApp.models import GroupActivityModel, ActivityPartModel, ActivityModel, GroupModel
from .forms import TaskForm
from .models import TaskModel, TaskPartsModel, TaskActivityModel, PartImageModel
from django.contrib.auth.decorators import login_required


@login_required
def task_list(request):
    # print(TaskModel.objects.filter(taskpartsmodel__user__exact=request.user))
    completedList = TaskModel.objects.all()
    completedList = [task for task in completedList if not task.isComplete()]

    return render(request, 'WorkOrdersApp/listTasks.html', {'header': 'Outstanding Tasks',
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
                                          task=taskMy,
                                          increment=required.increment,
                                          quantityRequired=required.quantity,
                                          quantityCompleted=0,
                                          )
                    temp.save()

            return redirect('tasks')
    else:
        form = TaskForm()
        return render(request, 'WorkOrdersApp/addTask.html', {'taskform': form})


@login_required
def info_task_activities(request, taskid):
    task = get_object_or_404(TaskModel, id=taskid)
    activities = TaskActivityModel.objects.filter(task=task, activity__workCenter__in=request.user.groups.all())

    if activities.count() == 1:
        activity = activities.first()
        return info_task_parts(request, taskid, activity.id)

    for activity in activities:
        activity.complete = activity.isComplete()
        partsRequired = TaskPartsModel.objects.filter(activity=activity)

        completedList = [part for part in partsRequired if not part.isComplete()]

        if len(completedList) > 0:
            activity.status = activity.activity.getStatus()
        else:
            activity.status = "Done"

    return render(request, 'WorkOrdersApp/infoTaskActivities.html', {'header': 'Grouped Activities',
                                                       'task': task,
                                                       'taskactivities': activities})


@login_required
def info_task_parts(request, taskid, taskactivityid):
    taskactivity = get_object_or_404(TaskActivityModel, id=taskactivityid)
    # for part in TaskPartsModel.objects.filter(task=taskid,activity=taskactivityid):
    #     print(str(part.quantityRequired)+" - "+str(part.quantityCompleted))
    # print(TaskActivityModel.isComplete(ac))

    if request.method == "POST":
        for completed in request.POST:
            try:
                updatedvalue = get_object_or_404(TaskPartsModel, id=int(completed))
                updatedvalue.updateQuantity(int(request.POST[completed]), request.user)
            except ValueError:
                pass

    taskPartsRequired = TaskPartsModel.objects.filter(task=taskid, activity=taskactivityid) \
        .filter(increment=False)
    for part in taskPartsRequired:
        part.thumbnail = PartImageModel.objects.filter(part=part.part).first()

    taskPartsProduced = TaskPartsModel.objects.filter(task=taskid, activity=taskactivityid) \
        .filter(increment=True)
    for part in taskPartsProduced:
        part.thumbnail = PartImageModel.objects.filter(part=part.part).first()

    context = {'header': 'Kits',
               'producedparts': taskPartsProduced,
               'requiredparts': taskPartsRequired,
               'taskid': taskid,
               'taskactivity': taskactivity}

    if get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Picking':
        return render(request, 'WorkOrdersApp/infoTaskPickingParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Lazer Cutting':
        for producedpart in taskPartsProduced:
            if producedpart.quantityCompleted == producedpart.quantityRequired:
                for requiredpart in taskPartsRequired:
                    requiredpart.quantityCompleted = requiredpart.quantityRequired
                    requiredpart.quantityCompleted
                    requiredpart.save()
                break
        return render(request, 'WorkOrdersApp/infoTaskLaserCuttingParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Powder Coating':
        return render(request, 'WorkOrdersApp/infoTaskParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Zinc Coating':
        return render(request, 'WorkOrdersApp/infoTaskParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Heat Treatment & Shot Peening':
        return render(request, 'WorkOrdersApp/infoTaskParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Brobo Rotary Saw':
        return render(request, 'WorkOrdersApp/infoTaskParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Shakeout':
        return render(request, 'WorkOrdersApp/infoTaskParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Sheet Metal Folding':
        return render(request, 'WorkOrdersApp/infoTaskParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Ordering':
        taskPartsOrdered = TaskPartsModel.objects.filter(task=taskid)
        return render(request, 'WorkOrdersApp/infoTaskOrderingParts.html', {'orderedparts': taskPartsOrdered,
                                                              'taskid': taskid,
                                                              'taskactivity': taskactivity})
    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Assembly':
        return render(request, 'WorkOrdersApp/infoTaskAssemblyParts.html', context)

    print(f'{get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name=}')

