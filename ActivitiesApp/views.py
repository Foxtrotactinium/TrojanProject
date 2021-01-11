from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView, DeleteView
from simple_history.utils import update_change_reason

from PartsApp.models import PartImageModel
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def activity_list(request):
    return render(request, 'ActivitiesApp/listActivities.html', {'header': 'ActivityModel',
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

        return render(request, 'ActivitiesApp/addActivity.html', {'activityform': form})


@login_required
def activity_information(request, id):
    activity = get_object_or_404(ActivityModel, id=id)

    if request.method == "POST":

        actform = activity_form(request.POST, instance=activity)
        insform = InstructionForm(request.POST, reques1t.FILES, instance=activity)
        print(request.FILES)
        if actform.is_valid():
            actform.save()
            return redirect('activityinformation', id)
        if insform.is_valid():
            print("hello")
            # insform.save()
            tempins = instruction(pdf=request.FILES["pdf"], activity=activity)
            tempins.save()
            return redirect('activityinformation', id)


        # for qty in request.POST[required.pk]:
        #     print(qty)
        #     try:
        #         updatedvalue = get_object_or_404(ActivityPartModel, id=int(completed))
        #         updatedvalue.updateQuantity(int(request.POST[completed])
        #     except ValueError:
        #         pass

    required = ActivityPartModel.objects.filter(activity=id).filter(increment=False).order_by('order')
    for part in required:
        part.thumbnail = PartImageModel.objects.filter(part=part.part).first()
    produced = ActivityPartModel.objects.filter(activity=id).filter(increment=True).order_by('order')
    for part in produced:
        part.thumbnail = PartImageModel.objects.filter(part=part.part).first()

    instructions = instruction.objects.filter(activity=activity)
    instructionform = InstructionForm(initial={'activity': activity})

    form = activity_form(instance=activity)
    context = {'activityform': form,
               'activitypartsrequired': required,
               'activitypartsproduced': produced,
               'instructions': instructions,
               'instructionform': instructionform,
               'activity': activity,
               'history': ActivityPartModel.history.filter(activity=activity)
               }
    print(activity)
    print(ActivityPartModel.history.model.objects.all())
    return render(request, 'ActivitiesApp/infoActivity.html', context)


@login_required
def add_required_part_to_activity(request, id, increment):
    activity = get_object_or_404(ActivityModel, id=id)
    activity_parts = ActivityPartModel.objects.filter(activity=id).filter(increment=increment)
    parts = PartModel.objects.all()
    form = required_part_form(initial={'activity': id, 'increment': increment})
    if increment == False:
        header = "Parts Required"
    else:
        header = "Parts Produced"
    context = {'activity': activity,
               'requiredpartform': form,
               'activityrequiredparts': activity_parts,
               'parts': parts,
               'header': header
               }

    if request.method == "POST":
        form = required_part_form(request.POST)

        if form.is_valid():
            form.save()
        return render(request, 'ActivitiesApp/addActivityPart.html', context)

    return render(request, 'ActivitiesApp/addActivityPart.html', context)


@require_POST
def save_new_ordering_parts_of_activity(request, id):
    form = PartOrderingForm(request.POST)

    if form.is_valid():
        ordered_ids = form.cleaned_data["ordering"].split(',')

        with transaction.atomic():
            current_order = 1
            for lookup_id in ordered_ids:
                group = ActivityPartModel.objects.get(id=lookup_id)
                group.order = current_order
                group.save()
                current_order += 1

    return redirect('activityinformation', id)


@login_required
def groups(request):
    # print(WorkCenterTypes.objects.filter(wcType=type))

    return render(request, 'ActivitiesApp/listGroups.html', {'header': 'GroupModel',
                                                             'groups': GroupModel.objects.all()})


@login_required
def add_group(request):
    if request.method == "POST":
        form = group_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('groups')

    else:
        form = group_form()
        return render(request, 'ActivitiesApp/addGroup.html', {'groupform': form})


@login_required
def group_information(request, id):
    group = get_object_or_404(GroupModel, id=id)
    activities = GroupActivityModel.objects.filter(group=id).values_list('activity', flat=True)
    parts = ActivityPartModel.objects.filter(activity__in=activities, increment=False)
    if request.method == "POST":
        form = group_form(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('groups')

    else:
        form = group_form(instance=group)
        context = {'groupform': form,
                   'groupactivities': GroupActivityModel.objects.filter(group=id).order_by('order'),
                   'id': id,
                   'parts':parts}
        return render(request, 'ActivitiesApp/infoGroups.html', context)


class GroupActivityDelete(DeleteView):
    # http_method_names = ['post']
    model = GroupActivityModel
    fields = "__all__"

    def get_success_url(self):
        return reverse('groupinformation', args=[str(self.object.group.pk)])


@login_required
def add_required_activity_to_group(request, id):
    activities = ActivityModel.objects.all()
    group_activities = GroupActivityModel.objects.filter(group=id)
    group = get_object_or_404(GroupModel, id=id)

    form = required_activity_form(initial={'group': id, 'order': 100_000})
    context = {'requiredactivityform': form,
               'grouprequiredactivity': group_activities,
               'allactivities': activities,
               'id': id
               }
    if request.method == "POST":
        form = required_activity_form(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'ActivitiesApp/addGroupActivity.html', context)

    return render(request, 'ActivitiesApp/addGroupActivity.html', context)


class ActivityPartUpdate(UpdateView):
    http_method_names = ['post']
    model = ActivityPartModel
    fields = ['quantity', 'location']

    def form_valid(self, form):
        oldObject = ActivityPartModel.objects.get(id=self.object.id)
        change_reason = []
        if 'quantity' in form.changed_data:
            change_reason.append(f'quantity updated from {oldObject.quantity} to {self.object.quantity}')

        if 'location' in form.changed_data:
            change_reason.append(f'extra info amended from {oldObject.location} to {self.object.location}')

        superReturn = super().form_valid(form)
        update_change_reason(self.object, f'{",".join(change_reason)}')
        return superReturn

    def get_success_url(self):
        return reverse('activityinformation', args=[str(self.object.activity.pk)])


class ActivityPartDelete(DeleteView):
    http_method_names = ['post']
    model = ActivityPartModel

    def get_success_url(self):
        return reverse('activityinformation', args=[str(self.object.activity.pk)])


@require_POST
def save_new_ordering_activities_of_group(request, id):
    form = OrderingForm(request.POST)

    if form.is_valid():
        ordered_ids = form.cleaned_data["ordering"].split(',')

        with transaction.atomic():
            current_order = 1
            for lookup_id in ordered_ids:
                group = GroupActivityModel.objects.get(id=lookup_id)
                group.order = current_order
                group.save()
                current_order += 1

    return redirect('groupinformation', id)

# @login_required
# def work_center(request):
#
#     return render(request, 'listWorkCenters.html', {'header': 'GroupModel',
#                                                     'workcenters': GroupModel.objects.all(),
#                                                     'types': WorkCenterTypes.objects.all()})

# # use for getting all files in instruction model relating to job from ActivityModel model
# some_manual = Manual.objects.get(id=1)
# some_manual_pdfs = some_manual.manualpdf_set.all()
