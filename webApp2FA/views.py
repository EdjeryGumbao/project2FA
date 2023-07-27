from django.shortcuts import render

# debugging (comment out later)
def base(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'layouts/base.html', context)

# debugging

def home(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'pages/home.html', context)

def login(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'pages/login.html', context)

def register(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'pages/register.html', context)

def profile(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'pages/profile.html', context)

def gallery(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'pages/gallery.html', context)

def intrudergallery(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'pages/intrudergallery.html', context)