from django import http
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView, DeleteView, CreateView

from ActivitiesApp.models import GroupActivityModel, ActivityPartModel, ActivityModel, GroupModel, instruction
from PartsApp.models import PartModel
from .forms import TaskForm, TaskActivityPartsForm
from .models import TaskModel, TaskPartsModel, TaskActivityModel, PartImageModel
from django.contrib.auth.decorators import login_required


@login_required
def task_list(request):
    # print(TaskModel.objects.filter(taskpartsmodel__user__exact=request.user))
    tasks = TaskModel.objects.all()
    # tasks = TaskModel.objects.filter(group__activity__workCenter__in=request.user.groups.all())
    # activeList = [task for task in tasks if not task.isComplete()]
    # completedList = [task for task in tasks if task.isComplete()]
    activeList = [task for task in tasks if not task.userGroupCompleted(request.user.groups.all())]
    completedList = [task for task in tasks if task.userGroupCompleted(request.user.groups.all())]

    return render(request, 'WorkOrdersApp/listTasks.html', {'header': 'Outstanding Tasks',
                                                            'activetasks': activeList,
                                                            'completedtasks': completedList})


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

            groupactivitylist = GroupActivityModel.objects.filter(group=groupname).order_by('order')

            for groupactivity in groupactivitylist:
                tempactivity = TaskActivityModel(task=taskMy,
                                                 activity=groupactivity.activity)
                tempactivity.save()
                required_list = ActivityPartModel.objects.filter(activity=groupactivity.activity).order_by('id')
                for required in required_list:
                    temp = TaskPartsModel(activity=tempactivity,
                                          part=required.part,
                                          task=taskMy,
                                          increment=required.increment,
                                          quantityRequired=required.quantity,
                                          order=required.order,
                                          extra=required.location,
                                          quantityCompleted=0,
                                          )
                    temp.save()

            return redirect('tasks')
    else:
        form = TaskForm()
        groups = GroupModel.objects.all()
        return render(request, 'WorkOrdersApp/addTask.html', {'taskform': form, 'groups': groups})


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


class TaskActivityDelete(DeleteView):
    # http_method_names = ['post']
    model = TaskActivityModel
    fields = "__all__"

    def get_success_url(self):
        return reverse('infotaskactivities', args=[str(self.object.task.pk)])


@login_required
def info_task_parts(request, taskid, taskactivityid):
    taskactivity = get_object_or_404(TaskActivityModel, id=taskactivityid)
    instructions = instruction.objects.filter(activity=taskactivity.activity)

    if request.method == "POST":
        for completed in request.POST:
            try:
                updatedvalue = get_object_or_404(TaskPartsModel, id=int(completed))
                updatedvalue.updateQuantity(int(request.POST[completed]), request.user)
            except ValueError:
                pass

    # activity_part_required = ActivityPartModel.objects.filter(activity=taskactivity.activity, increment=False).order_by('order')
    #
    # activity_part_produced = ActivityPartModel.objects.filter(activity=taskactivity.activity, increment=True).order_by('order')

    taskPartsRequired = TaskPartsModel.objects.filter(task=taskid, activity=taskactivityid, increment=False).order_by('order')
    for part in taskPartsRequired:
        part.thumbnail = PartImageModel.objects.filter(part=part.part).first()
        part.low = part.part.stockOnHand < part.part.minimumStock

    taskPartsProduced = TaskPartsModel.objects.filter(task=taskid, activity=taskactivityid, increment=True).order_by('order')
    for part in taskPartsProduced:
        part.thumbnail = PartImageModel.objects.filter(part=part.part).first()
        part.low = part.part.stockOnHand < part.part.minimumStock

    # for (a_part, t_part) in zip(activity_part_required, taskPartsRequired):
    #     t_part.thumbnail = PartImageModel.objects.filter(part=t_part.part).first()
    #     t_part.extra = a_part
    #
    # for (a_part, t_part) in zip(activity_part_produced, taskPartsProduced):
    #     t_part.thumbnail = PartImageModel.objects.filter(part=t_part.part).first()
    #     t_part.extra = a_part


    # taskPartsRequired = TaskPartsModel.objects.filter(task=taskid, activity=taskactivityid) \
    #     .filter(increment=False)
    # for part in taskPartsRequired:
    #     part.thumbnail = PartImageModel.objects.filter(part=part.part).first()
    #     .order_by('id')
    #     required_list = ActivityPartModel.objects.filter(activity=groupactivity.activity).order_by('id')
    #
    #
    #     ActivityPartModel.objects.filter(activity=taskactivity.activity).filter(part=part).order_by('id')
    #
    #     part.extra = ActivityPartModel.objects.filter(part=part.part).filter(activity__activityName=taskactivity).first()
    #
    # taskPartsProduced = TaskPartsModel.objects.filter(task=taskid, activity=taskactivityid) \
    #     .filter(increment=True)
    # for part in taskPartsProduced:
    #     part.thumbnail = PartImageModel.objects.filter(part=part.part).first()
    #     part.extra = ActivityPartModel.objects.filter(part=part.part).filter(activity__activityName=taskactivityid).first()

    context = {'header': 'Kits',
               'producedparts': taskPartsProduced,
               'requiredparts': taskPartsRequired,
               'taskid': taskid,
               'taskactivity': taskactivity,
               'instructions': instructions}

    if get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Picking':
        return render(request, 'WorkOrdersApp/infoTaskPickingParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Lazer Cutting':
        for producedpart in taskPartsProduced:
            if producedpart.quantityCompleted == producedpart.quantityRequired:
                for requiredpart in taskPartsRequired:
                    requiredpart.quantityCompleted = requiredpart.quantityRequired
                    # requiredpart.quantityCompleted
                    requiredpart.save()
                break
        return render(request, 'WorkOrdersApp/infoTaskLaserCuttingParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Powder Coating':
        return render(request, 'WorkOrdersApp/infoTaskPowderCoatingParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Zinc Coating':
        return render(request, 'WorkOrdersApp/infoTaskZincCoatingParts.html', context)

    elif get_object_or_404(TaskActivityModel,
                           id=taskactivityid).activity.workCenter.name == 'Heat Treatment & Shot Peening':
        return render(request, 'WorkOrdersApp/infoTaskParts.html', context)

    elif get_object_or_404(TaskActivityModel,
                           id=taskactivityid).activity.workCenter.name == 'Welding':
        return render(request, 'WorkOrdersApp/infoTaskLaserCuttingParts.html', context)

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
        for requiredpart in taskPartsRequired:
            if requiredpart.quantityCompleted == requiredpart.quantityRequired:
                for producedpart in taskPartsProduced:
                    producedpart.quantityCompleted = producedpart.quantityRequired
                    # producedpart.quantityCompleted
                    producedpart.save()
                break
        return render(request, 'WorkOrdersApp/infoTaskAssemblyParts.html', context)

    elif get_object_or_404(TaskActivityModel, id=taskactivityid).activity.workCenter.name == 'Hose Cutting':
        for requiredpart in taskPartsRequired:
            if requiredpart.quantityCompleted == requiredpart.quantityRequired:
                for producedpart in taskPartsProduced:
                    producedpart.quantityCompleted = producedpart.quantityRequired
                    # producedpart.quantityCompleted
                    producedpart.save()
                break
        return render(request, 'WorkOrdersApp/infoTaskHoseCuttingParts.html', context,)


def info_task_part_include(request, taskid, taskactivityid, increment):
    taskactivity = get_object_or_404(TaskActivityModel, id=taskactivityid)
    task = get_object_or_404(TaskModel, id=taskid)
    taskparts = TaskPartsModel.objects.filter(task=task, activity=taskactivity)
    parts = PartModel.objects.all()

    if request.method == 'POST':
        form = TaskActivityPartsForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return info_task_parts(request, taskid, taskactivityid)

    initial = {'activity': taskactivity,
               'task': task,
               'increment': increment,
               'quantityCompleted': 0,
               'order': 100_000,
               'user': request.user
               }
    form = TaskActivityPartsForm(initial=initial)
    context = {"parts": parts,
               "partform": form,
               "taskparts": taskparts,
               "task": task,
               "taskactivity": taskactivity}

    return render(request, 'WorkOrdersApp/addTaskActivityParts.html', context)


class TaskPartRequiredUpdate(UpdateView):
    http_method_names = ['post']
    model = TaskPartsModel
    fields = ['quantityRequired']

    def get_success_url(self):
        return reverse('infotaskparts', args=[str(self.object.task.pk), str(self.object.activity.pk)])

class TaskPartSerialUpdate(UpdateView):
    http_method_names = ['post']
    model = TaskPartsModel
    fields = ['serial']

    def get_success_url(self):
        return reverse('infotaskparts', args=[str(self.object.task.pk), str(self.object.activity.pk)])

class TaskPartCompletedUpdate(UpdateView):
    # http_method_names = ['post']
    model = TaskPartsModel
    fields = ['quantityCompleted']

    def get_success_url(self):
        return reverse('infotaskparts', args=[str(self.object.task.pk), str(self.object.activity.pk)])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            taskPart = get_object_or_404(TaskPartsModel, id=int(self.object.pk))
            taskPart.updateQuantity(self.object.quantityCompleted, request.user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TaskPartDelete(DeleteView):
    # http_method_names = ['post']
    model = TaskPartsModel
    fields = "__all__"

    def get_success_url(self):
        return reverse('infotaskparts', args=[str(self.object.task.pk), str(self.object.activity.pk)])


class TaskActivityCreate(CreateView):
    model = TaskActivityModel
    fields = ('activity',)

    # def get_initial(self):
    #     task = get_object_or_404(TaskModel, id=self.kwargs.get('taskid'))
    #     return {'task': task}

    def form_valid(self, form):
        task = get_object_or_404(TaskModel, id=self.kwargs.get('taskid'))
        form.instance.task = task

        tempactivity = form.save()

        activity = tempactivity.activity

        required_list = ActivityPartModel.objects.filter(activity=activity)
        for required in required_list:
            temp = TaskPartsModel(activity=tempactivity,
                                  part=required.part,
                                  task=task,
                                  increment=required.increment,
                                  quantityRequired=required.quantity,
                                  order=required.order,
                                  extra=required.location,
                                  quantityCompleted=0,
                                  )
            temp.save()

        # return super(TaskActivityCreate, self).form_valid(form)
        return http.HttpResponseRedirect(reverse('infotaskactivities', args=[str(task.pk)]))
        # return reverse('infotaskactivities', args=[str(task.pk)])

    # def get_success_url(self):
    #     return reverse('infotaskactivities', args=[str(self.object.task.pk)])
