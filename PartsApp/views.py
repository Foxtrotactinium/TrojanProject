# Create your views here.
from django.db.models import Sum
from django.shortcuts import render, redirect

from ActivitiesApp.models import GroupActivityModel, ActivityModel, ActivityPartModel
from WorkOrdersApp.forms import TaskForm, TaskPartsModel
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group


# Create your views here.
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


@login_required
def list_supplier(request):
    context = {
        'header': 'Supplier List',
        'suppliers': SupplierModel.objects.all(),
    }
    return render(request, 'PartsApp/listSuppliers.html', context)


@login_required
def info_part(request, part_id):
    part = PartModel.objects.all().filter(pk=part_id).first()

    if request.method == "POST":
        imageform = ImageForm(request.POST, request.FILES, initial={'part': part})
        form1 = PartForm(request.POST, instance=part)
        form2 = PartCommentForm(request.POST, initial={'author': request.user, 'part': part})
        if form1.is_valid():
            form1.save()
        if form2.is_valid():
            form2.save()
        if imageform.is_valid():
            imageform.save()



    imageform = ImageForm(initial={'part': part})
    image = PartImageModel.objects.filter(part=part)
    form1 = PartForm(instance=part)
    form2 = PartCommentForm(initial={'author': request.user, 'part': part})
    movements = part.history.all()
    previouslevel = 0
    activities = GroupActivityModel.objects.filter(activity__activitypartmodel__part=part)

    for activity in activities:
        activity.qty = ActivityPartModel.objects.filter(activity=activity.activity, part=part).aggregate(
            Sum("quantity"))

    for movement in movements:
        movement.change = movement.stockOnHand - previouslevel
        previouslevel = movement.stockOnHand

    # print(movements.filter(change__lt=0,change__gt=0))
    # filtered = (x for x in movements if x.change != 0)
    # print(movements.exclude(change=0))
    # print(filtered.count())
    context = {'partform': form1,
               'images': image,
               'imageform': imageform,
               'partsuppliers': PartSupplierModel.objects.all().filter(
                   part=part.id),
               'commentForm': form2,
               'part_id': part.id,
               'movements': movements,
               'activities': activities,
               'partcomments': PartCommentModel.objects.all().filter(part=part.id),
               }

    return render(request, 'PartsApp/infoPart.html', context)


@login_required
def info_supplier(request, id):
    supplierparts = PartSupplierModel.objects.filter(supplier=id)
    if request.method == "POST":
        if 'supplier' in request.POST:
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
            return redirect('inventory')

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
