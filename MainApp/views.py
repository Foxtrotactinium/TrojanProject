from django.shortcuts import render,  redirect

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def register(request):
    if request.method == "POST":
        login_form = UserCreationForm(request.POST)
        if login_form.is_valid():
            user = login_form.save()
            username = login_form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("inventory")

        else:
            for msg in login_form.error_messages:
                messages.error(request, f"{msg}: {login_form.error_messages[msg]}")

            return render(request=request,
                          template_name="MainApp/register.html",
                          context={"login_form": login_form})

            login_form = UserCreationForm
        return render(request=request,
                      template_name="MainApp/register.html",
                      context={"login_form": login_form})
    else:
        login_form = UserCreationForm
        return render(request=request,
                      template_name="MainApp/register.html",
                      context={"login_form": login_form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("inventory")


def composer_test(request):
    return render(request, "MainApp/composerplayertest.html")


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
                  template_name="MainApp/login.html",
                  context={"login_form": login_form})