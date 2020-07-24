from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.
def inventory_list(request):
    parts = PartsList.objects.all()
    for part in parts:
        all_suppliers = PartSuppliers.objects.all().filter(partnumber=part.id)
        if all_suppliers.count() > 1:
            part.supplier = all_suppliers.get_object_or_404(preferred=True)

        else:
            part.supplier = all_suppliers.first()

    context = {
        'parts': parts,
        'header': 'Inventory'
    }

    return render(request, 'listParts.html', context)

def supplier_list(request):
    context = {
        'header': 'Supplier List',
        'suppliers': Suppliers.objects.all(),
    }
    return render(request, 'listSuppliers.html', context)

def part_information(request, id):
    part = PartsList.objects.all().filter(pk=id).first()

    if request.method == "POST":
        form1 = part_form(request.POST, instance=part)
        form2 = part_comment_form(request.POST, initial={'author': request.user, 'part': part})
        if form1.is_valid():
            form1.save()
            return redirect('inventory')
        if form2.is_valid():
            form2.save()
            return redirect('inventory')

    else:
        form1 = part_form(instance=part)
        form2 = part_comment_form(initial={'author': request.user, 'part': part})
        return render(request, 'infoPart.html', {'partform': form1,
                                               'partsuppliers': PartSuppliers.objects.all().filter(partnumber=part.id),
                                               'commentForm': form2,
                                               'partcomments': PartComments.objects.all().filter(part=part.id),
                                                 })

def supplier_information(request, id):
    if request.method == "POST":
        form = supplier_form(request.POST, instance=Suppliers.objects.all().filter(pk=id).first())
        if form.is_valid():
            form.save()
            return redirect('suppliers')

    else:
        form = supplier_form(instance=Suppliers.objects.all().filter(pk=id).first())
        return render(request, 'infoSupplier.html', {'supplierForm': form,
                                                 'supplierparts': PartSuppliers.objects.all().filter(partsupplier=id)})

def add_supplier(request):
    if request.method == "POST":
        form = supplier_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('suppliers')

    else:
        form = supplier_form()
        return render(request, 'addSupplier.html', {'supplierForm': form})


def add_part(request):
    if request.method == "POST":
        form = part_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('inventory')

    else:
        form = part_form()
        return render(request, 'addPart.html', {'PartForm': form})
