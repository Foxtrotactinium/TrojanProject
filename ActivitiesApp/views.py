from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import activity_form, required_part_form, task_form, required_activity_form
from django.contrib import messages
from django.utils import timezone


# Create your views here.
def activity_list(request):
    return render(request, 'activities.html', {'header': 'ActivityModel',
                                               'activities': ActivityModel.objects.all()})


def add_activity(request):
    if request.method == "POST":
        form = activity_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('activities')

    else:
        form = activity_form()

        return render(request, 'addactivity.html', {'activityform': form})


def activity_information(request, id):
    activity = get_object_or_404(ActivityModel, id=id)

    if request.method == "POST":
        form = activity_form(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activities')

    else:
        form = activity_form(instance=activity)
        # print(ActivityPartModel.objects.all().filter(activity=id))
        context = {'activityform': form,
                   'activitypartsrequired': ActivityPartModel.objects.all().filter(activity=id),
                   'id': id}
        return render(request, 'activityinformation.html', context)


def add_required_part_to_activity(request, id):
    activity_parts = ActivityPartModel.objects.all().filter(activity=id)

    parts = PartModel.objects.all()
    if request.method == "POST":
        form = required_part_form(request.POST)

        # print(form.is_valid(), form.errors)

        if form.is_valid():
            form.save()
        return redirect('activities')

    else:
        form = required_part_form(initial={'activity': id})
        # form.fields['activityName'].disabled = True
        context = {'requiredpartform': form,
                   'activityrequiredparts': activity_parts,
                   'parts': parts,
                   }
    return render(request, 'addrequired.html', context)


def tasks(request):
    return render(request, 'tasks.html', {'header': 'TaskModel',
                                          'tasks': TaskModel.objects.distinct()})


def add_task(request):
    if request.method == "POST":
        form = task_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('tasks')
        # if form.is_valid():
        #     taskName = form.cleaned_data['taskName']
        #     activity = form.cleaned_data['activityName']
        #
        #     if TaskModel.objects.filter(taskName=taskName).count() > 0:
        #         messages.error(request, "Task name exists")
        #         return redirect('addtask')
        #
        #     required_list = ActivityPartModel.objects.filter(activityName=activity)
        #     for required in required_list:
        #         temp = TaskActivityModel(taskName=taskName,
        #                                       activityName=activity,
        #                                       )
        #         temp.save()
        #     return redirect('tasks')
    else:
        form = task_form()
        return render(request, 'addtask.html', {'taskform': form})


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
        return render(request, 'taskinformation.html', context)


def add_required_activity_to_task(request, id):
    all_activities = ActivityModel.objects.all()
    task_activities = TaskActivityModel.objects.filter(task=id)
    if request.method == "POST":
        form = required_activity_form(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print(form)
            form.save()
        return redirect('tasks')

    else:
        form = required_activity_form(initial={'taskName': id})
        # form.fields['taskName'].readonly = True
        # form.fields['taskName'].value = id
        context = {'requiredactivityform': form,
                   'taskrequiredactivity': task_activities,
                   'allactivities': all_activities,
                   }
    return render(request, 'addrequiredactivity.html', context)


def tasks(request):
    return render(request, 'tasks.html', {'header': 'TaskModel',
                                          'tasks': TaskModel.objects.all()})

# # use for getting all files in instruction model relating to job from ActivityModel model
# some_manual = Manual.objects.get(id=1)
# some_manual_pdfs = some_manual.manualpdf_set.all()
