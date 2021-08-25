# Create your views here.
from functools import reduce

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView, UpdateView
from BrotherQL270NW.imageTest import print_label
from ActivitiesApp.models import ActivityPartModel
from WorkOrdersApp.models import TaskModel
from WorkOrdersApp.forms import TaskForm, TaskPartsModel
from .forms import *


# Create your views here.
@login_required
def qr_scan(request):
    searchQuery = request.GET.get('q', None)
    fields = request.GET.keys()
    context = {
        'header': 'Scanner',
        'infoText': 'Please scan first'
    }
    if searchQuery is not None and searchQuery != '':

        parts = None
        query = Q()
        if 'partnumbercheck' in fields:
            query.add( Q(partNumber__contains=searchQuery), Q.OR)

        if 'descriptioncheck' in fields:
            query.add(Q(description__contains=searchQuery), Q.OR)

        if 'locationcheck' in fields:
            query.add(Q(location__contains=searchQuery), Q.OR)



        if len(query) == 0:
            context['infoText'] = f'Nothing found, please select a checkbox'
            return render(request, 'PartsApp/partsQrScan.html', context)

        parts = PartModel.objects.filter(query)

        if parts == None or parts.count() == 0:
            context['infoText'] = f'Nothing found for partNumber "{searchQuery}"'
        elif parts.count() == 1:

            part = parts.first()

            return redirect('info_part', part.id)  # info_part(request, part.id)

        else:
            # print(f'{parts=}')

            for part in parts:
                part.low = part.stockOnHand < part.minimumStock
            for part in parts:
                part.supplier = part.getPreferredSupplier()

            context = {
                'parts': parts,
                'header': 'Inventory'
            }

            return render(request, 'PartsApp/partsQrScan.html', context)

    return render(request, 'PartsApp/partsQrScan.html', context)


@login_required
def list_parts(request):
    parts = PartModel.objects.all()
    for part in parts:
        part.low = part.stockOnHand < part.minimumStock
    for part in parts:
        part.supplier = part.getPreferredSupplier()

    context = {
        'parts': parts,
        'header': 'Inventory'
    }

    return render(request, 'PartsApp/listParts.html', context)


class PartHistoryListView(ListView):
    model = PartModel.history.model

    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    # def get_queryset(self):
    #     model = PartModel.objects.history.all()
    #     for part in model:
    #         part.change = part.stockOnHand - part.prev_record.stockOnHand
    #         print(part.change)
    #     return model


@login_required
def list_supplier(request):
    context = {
        'header': 'Supplier List',
        'suppliers': SupplierModel.objects.all(),
    }
    return render(request, 'PartsApp/listSuppliers.html', context)


def print_inventory_label(request, part_id):
    part = PartModel.objects.get(id=part_id)
    print_label(part.partNumber, part.description)
    return redirect("info_part", part_id)


@login_required
def info_part(request, part_id):
    part = PartModel.objects.all().filter(pk=part_id).first()

    if request.method == "POST":
        imageform = ImageForm(request.POST, request.FILES, initial={'part': part})
        form1 = PartForm(request.POST, instance=part)
        form2 = PartCommentForm(request.POST, initial={'author': request.user, 'part': part})
        if form1.is_valid():
            part = form1.save()
            # update_change_reason(part, 'Manual')
        if form2.is_valid():
            form2.save()
        if imageform.is_valid():
            imageform.save()

    imageform = ImageForm(initial={'part': part})
    image = PartImageModel.objects.filter(part=part)
    form1 = PartForm(instance=part)
    # taskform = LowStockTaskForm(instance=part)
    form2 = PartCommentForm(initial={'author': request.user, 'part': part})
    movements = part.history.all().reverse()
    previouslevel = 0
    # activities = GroupActivityModel.objects.filter(activity__activitypartmodel__part=part)
    #
    # for activity in activities:
    #     activity.qty = ActivityPartModel.objects.filter(activity=activity.activity, part=part).aggregate(
    #         Sum("quantity"))

    activities = ActivityPartModel.objects.filter(part=part)

    for movement in movements:
        movement.change = movement.stockOnHand - previouslevel
        previouslevel = movement.stockOnHand

    context = {'partform': form1,
               'part': part,
               'images': image,
               'imageform': imageform,
               'partsuppliers': PartSupplierModel.objects.filter(
                   part=part.id),
               'commentForm': form2,
               'part_id': part.id,
               'movements': reversed(movements),
               'activities': activities,
               'partcomments': PartCommentModel.objects.all().filter(part=part.id),
               }

    return render(request, 'PartsApp/infoPart.html', context)


@login_required
def low_stock_group(request, part_id):
    groups = GroupModel.objects.all()
    part = PartModel.objects.filter(pk=part_id)
    if request.method == "POST":
        form = LowStockGroupForm(request.POST)
        print('======'*2)
        print(form)
        if form.is_valid():
            form.save()
        return redirect('info_part', part_id)

    else:
        form = LowStockGroupForm(initial={'PartModel': part,})
        # print(form)
        context = {'LowStockGroupForm': form,
                   'part': part,
                   'groups': groups,
                   }
    return render(request, 'PartsApp/lowstockgroup.html', context)

class SupplierPartNumberUpdate(UpdateView):
    http_method_names = ['post']
    model = PartSupplierModel
    fields = ['supplierPartNumber']

    def get_success_url(self):
        return reverse('info_part', args=[str(self.object.part.pk)])


@login_required
def info_supplier(request, id):
    supplierparts = PartSupplierModel.objects.filter(supplier=id)
    if request.method == "POST":
        if 'supplierform-supplierName' in request.POST:
            supplierform = SupplierForm(request.POST, instance=SupplierModel.objects.filter(pk=id),
                                        prefix='supplierform')
            if supplierform.is_valid():
                supplierform.save()
                return redirect('suppliers')
        elif 'taskForm-taskName' in request.POST:
            taskform = TaskForm(request.POST, prefix='taskForm')
            if taskform.is_valid():
                ordertask = taskform.save()
                for part in supplierparts:
                    quantity = int(request.POST.get(f'{part.part.pk}'))
                    if quantity > 0:
                        temp = TaskPartsModel(task=ordertask,
                                              part=part.part,
                                              increment=True,
                                              quantityRequired=quantity,
                                              quantityCompleted=0,
                                              )
                        temp.save()

            return redirect('suppliers')

    else:
        for part in supplierparts:
            part.low = part.part.stockOnHand < part.part.minimumStock
            part.ordered = 0
        supplierform = SupplierForm(instance=SupplierModel.objects.all().filter(pk=id).first(), prefix='supplierform')
        taskform = TaskForm(prefix='taskForm')
        return render(request, 'PartsApp/infoSupplier.html', {'supplierform': supplierform,
                                                              'supplierparts': supplierparts,
                                                              'taskform': taskform})


@login_required
def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('suppliers')

    else:
        form = SupplierForm()
        return render(request, 'PartsApp/addSupplier.html', {'supplierForm': form})


@login_required
def add_part(request):
    if request.method == "POST":
        form = PartForm(request.POST)

        if form.is_valid():
            form.save()
            partnumber = form.cleaned_data['partNumber']
            part_id = PartModel.objects.get(partNumber__exact=partnumber)
            return info_part(request, part_id.id)

    else:
        form = PartForm()
        return render(request, 'PartsApp/addPart.html', {'PartForm': form})


@login_required
def add_supplier_to_part(request, part_id):
    suppliers = SupplierModel.objects.all()
    part = PartModel.objects.filter(pk=part_id)
    partsuppliers = PartSupplierModel.objects.filter(part=part_id)
    if request.method == "POST":
        form = PartSupplierForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('info_part', part_id)

    else:
        form = PartSupplierForm(initial={'part': part_id})
        context = {'partsupplierform': form,
                   'partsuppliers': partsuppliers,
                   'part': part,
                   'suppliers': suppliers,
                   }
    return render(request, 'PartsApp/addPartSupplier.html', context)
