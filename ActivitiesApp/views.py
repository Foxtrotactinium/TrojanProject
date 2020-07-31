from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import activity_form, required_part_form, task_form, required_activity_form
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def activity_list(request):
    return render(request, 'listActivities.html', {'header': 'ActivityModel',
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

        return render(request, 'addActivity.html', {'activityform': form})


@login_required
def activity_information(request, id):
    activity = get_object_or_404(ActivityModel, id=id)

    if request.method == "POST":
        form = activity_form(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activities')

    else:
        form = activity_form(instance=activity)
        context = {'activityform': form,
                   'activitypartsrequired': ActivityPartModel.objects.filter(activity=id).filter(increment=False),
                   # 'activitypartsproduced': ActivityPartModel.objects.filter(activity=id).filter(increment=True),
                   'id': id}
        return render(request, 'infoActivity.html', context)


@login_required
def add_required_part_to_activity(request, id, increment):
    activity_parts = ActivityPartModel.objects.filter(activity=id).filter(increment=increment)
    parts = PartModel.objects.all()
    if request.method == "POST":
        form = required_part_form(request.POST)

        if form.is_valid():
            form.save()
        return redirect('activities')

    else:
        form = required_part_form(initial={'activity': id})
        context = {'requiredpartform': form,
                   'activityrequiredparts': activity_parts,
                   'parts': parts,
                   }
    return render(request, 'addActivityPart.html', context)


@login_required
def tasks(request):
    return render(request, 'listTasks.html', {'header': 'TaskModel',
                                              'tasks': TaskModel.objects.distinct()})


@login_required
def add_task(request):
    if request.method == "POST":
        form = task_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('tasks')

    else:
        form = task_form()
        return render(request, 'addTask.html', {'taskform': form})


@login_required
def task_information(request, id):
    task = get_object_or_404(TaskModel, id=id)
    if request.method == "POST":
        form = task_form(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')

    else:
        form = task_form(instance=task)
        context = {'taskform': form,
                   'taskactivities': TaskActivityModel.objects.filter(task=id),
                   'id': id}
        return render(request, 'infoTask.html', context)


@login_required
def add_required_activity_to_task(request, id):
    activities = ActivityModel.objects.all()
    task_activities = TaskActivityModel.objects.filter(task=id)
    if request.method == "POST":
        form = required_activity_form(request.POST)
        if form.is_valid():
            form.save()
        return redirect('tasks')

    else:
        form = required_activity_form(initial={'task': id})
        context = {'requiredactivityform': form,
                   'taskrequiredactivity': task_activities,
                   'allactivities': activities,
                   }
    return render(request, 'addTaskActivity.html', context)


@login_required
def tasks(request):
    return render(request, 'listTasks.html', {'header': 'TaskModel',
                                              'tasks': TaskModel.objects.all()})

# # use for getting all files in instruction model relating to job from ActivityModel model
# some_manual = Manual.objects.get(id=1)
# some_manual_pdfs = some_manual.manualpdf_set.all()
