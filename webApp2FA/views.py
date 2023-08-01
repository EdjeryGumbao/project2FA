from django.shortcuts import render, redirect

# authentication for user table modules #
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from .forms import RegisterUserImage

# authentication #
def login_user (request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
            # Redirect to a success page.
        else:
            messages.error(request, ('Incorrect credentials, Please try again'))
            return redirect('login')
    
    else:
        return render(request, 'pages/auth/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        # imageform = RegisterUserImage(request.POST, request.FILES)
        if form.is_valid() and imageform.is_valid():
            # saves user account
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)

            # saves image
            # imageform.save()
            

            return redirect('home')
    else:
        form = RegisterUserForm()
        # imageform = RegisterUserImage()

    return render(request, 'pages/auth/register.html', {'form': form,})

# debugging (comment out later)
# def base(request):
#     context={} # This is a dictionary, You can add DB tables values here later
#     return render(request, 'layouts/base.html', context)

# debugging


# templates #

# def login(request):
#     context={} # This is a dictionary, You can add DB tables values here later
#     return render(request, 'pages/authentication/login.html', context)

# def register(request):
#     context={} # This is a dictionary, You can add DB tables values here later
#     return render(request, 'pages/auth/register.html', context)

def home(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'pages/home.html', context)

def profile(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'pages/profile.html', context)

def gallery(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'pages/gallery.html', context)

def intrudergallery(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'pages/intrudergallery.html', context)