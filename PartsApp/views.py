# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def list_parts(request):
    parts = PartModel.objects.all()
    for part in parts:
        all_suppliers = PartSupplierModel.objects.all().filter(part=part.id)
        if all_suppliers.count() > 1:
            part.supplierName = all_suppliers.get_object_or_404(preferred=True)
        else:
            part.supplierName = all_suppliers.first()

    context = {
        'parts': parts,
        'header': 'Inventory'
    }

    return render(request, 'listParts.html', context)


@login_required
def list_supplier(request):
    context = {
        'header': 'Supplier List',
        'suppliers': SupplierModel.objects.all(),
    }
    return render(request, 'listSuppliers.html', context)


@login_required
def info_part(request, part_id):
    part = PartModel.objects.all().filter(pk=part_id).first()

    if request.method == "POST":
        form1 = PartForm(request.POST, instance=part)
        form2 = PartCommentForm(request.POST, initial={'author': request.user, 'part': part})
        if form1.is_valid():
            form1.save()
            return redirect('inventory')
        if form2.is_valid():
            form2.save()
            return redirect('inventory')

    else:
        form1 = PartForm(instance=part)
        form2 = PartCommentForm(initial={'author': request.user, 'part': part})
        return render(request, 'infoPart.html', {'partform': form1,
                                                 'partsuppliers': PartSupplierModel.objects.all().filter(
                                                     part=part.id),
                                                 'commentForm': form2,
                                                 'part_id': part.id,
                                                 'partcomments': PartCommentModel.objects.all().filter(part=part.id),
                                                 })


@login_required
def info_supplier(request, id):
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=SupplierModel.objects.all().filter(pk=id).first())
        if form.is_valid():
            form.save()
            return redirect('suppliers')

    else:
        form = SupplierForm(instance=SupplierModel.objects.all().filter(pk=id).first())
        return render(request, 'infoSupplier.html', {'supplierForm': form,
                                                     'supplierparts': PartSupplierModel.objects.all().filter(
                                                         supplier=id)})


@login_required
def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('suppliers')

    else:
        form = SupplierForm()
        return render(request, 'addSupplier.html', {'supplierForm': form})


@login_required
def add_part(request):
    if request.method == "POST":
        form = PartForm(request.POST)

        if form.is_valid():
            form.sav0e()
            return redirect('inventory')

    else:
        form = PartForm()
        return render(request, 'addPart.html', {'PartForm': form})


@login_required
def add_supplier_to_part(request, part_id):
    suppliers = SupplierModel.objects.all()
    part = PartModel.objects.filter(pk=part_id)
    partsuppliers = PartSupplierModel.objects.filter(part=part_id)
    if request.method == "POST":
        form = PartSupplierForm(request.POST)
        if form.is_valid():
            part_supplier = form.save()

            is_preferred = form.cleaned_data['preferred']

            if is_preferred:
                part_supplier.setPreferred()

        return redirect('info_part', part_id)

    else:
        form = PartSupplierForm(initial={'part': part})
        context = {'partsupplierform': form,
                   'partsuppliers': partsuppliers,
                   'part': part,
                   'suppliers': suppliers,
                   }
    return render(request, 'addPartSupplier.html', context)
