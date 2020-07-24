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

    return render(request, 'inventory.html', context)

def supplier_list(request):
    context = {
        'header': 'Supplier List',
        'suppliers': Suppliers.objects.all(),
    }
    return render(request, 'suppliers.html', context)

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
        return render(request, 'detail.html', {'partform': form1,
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
        return render(request, 'supplier.html', {'supplierForm': form,
                                                 'supplierparts': PartSuppliers.objects.all().filter(partsupplier=id)})

def add_supplier(request):
    if request.method == "POST":
        form = supplier_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('suppliers')

    else:
        form = supplier_form()
        return render(request, 'addsupplier.html', {'supplierForm': form})


def add_part(request):
    if request.method == "POST":
        form = part_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('inventory')

    else:
        form = part_form()
        return render(request, 'addpart.html', {'PartForm': form})


def register(request):
    if request.method == "POST":
        login_form = UserCreationForm(request.POST)
        if login_form.is_valid():
            user = login_form.save()
            username = login_form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("inventory:inventory")

        else:
            for msg in login_form.error_messages:
                messages.error(request, f"{msg}: {login_form.error_messages[msg]}")

            return render(request=request,
                          template_name="register.html",
                          context={"login_form": login_form})

            login_form = UserCreationForm
        return render(request=request,
                      template_name="register.html",
                      context={"login_form": login_form})
    else:
        login_form = UserCreationForm
        return render(request=request,
                      template_name="register.html",
                      context={"login_form": login_form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("inventory")


def login_request(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('inventory')

            else:
                messages.error(request, "Invalid username or password.")

        else:
            messages.error(request, "Invalid username or password.")

    login_form = AuthenticationForm()
    return render(request=request,
                  template_name="login.html",
                  context={"login_form": login_form})
