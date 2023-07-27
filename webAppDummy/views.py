from django.shortcuts import render

def Dashboard(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'Dashboard.html', context)

def Login(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'Login.html', context)

def Register(request):
    context={} # This is a dictionary, You can add DB tables values here later
    return render(request, 'Register.html', context)

def test(request):
    return render(request, 'test.html')