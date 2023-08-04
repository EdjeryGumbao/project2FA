from django.shortcuts import render, redirect
from django.core.paginator import Paginator

# authentication for user table modules #
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib import messages
from .forms import RegisterUserForm
from .models import UserImage
from .models import WebsiteList
from .models import IntruderImage

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required


# authentication #
def login_user (request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Redirect the user to the next URL or a default URL
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
            # Redirect to a success page.
        else:
            messages.error(request, ('Incorrect credentials, Please try again'))
            return redirect('login_user')
    
    else:
        return render(request, 'pages/auth/login.html')

def logout_user(request):
    logout(request)
    return redirect('login_user')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST, request.FILES)
        # imageform = RegisterUserImage(request.POST, request.FILES)
        if form.is_valid():
            # Save the user account
            user = form.save()

            # Authenticate the user
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])

            # saves image
            userImage = UserImage()
            userImage.userID = user
            userImage.userImage = request.FILES.get('image')
            userImage.save()

            login(request, user)

            return redirect('home')
    else:
        form = RegisterUserForm()
        # imageform = RegisterUserImage()

    return render(request, 'pages/auth/register.html', {'form': form,})

@login_required(login_url='login_user')
def home(request):
    context = {}
    if request.method == 'POST':
        websiteListID = request.POST['websiteListID']
        if request.POST['button'] == 'edit':
            pass
        elif request.POST['button'] == 'delete':
            try :
                website = WebsiteList.objects.get(websiteListID=websiteListID)
                website.delete()
                context['alert_error'] = 'Website Successfully Deleted'
            except WebsiteList.DoesNotExist:
                pass
    website_list = WebsiteList.objects.all()

    # Set the number of items to display per page
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(website_list, items_per_page)

    # Get the current page number from the request
    page_number = request.GET.get('page')

    # Get the items for the current page
    page_obj = paginator.get_page(page_number)

    # Pass the paginated data to the template context
    context['page_obj'] = page_obj

    return render(request, 'pages/home.html', context)

@login_required(login_url='login_user')
def add_website(request):
    context={} # This is a dictionary, You can add DB tables values here later
    if request.method == 'POST':
        # Website Registration
        websiteName = request.POST['websiteName']
        websiteUrl = request.POST['websiteUrl']
        userID = request.user
        
        new_WebsiteList = WebsiteList(websiteName=websiteName, websiteUrl=websiteUrl, userID=userID)
        new_WebsiteList.save()
        return redirect('home')
    else:
        return render(request, 'pages/add_website.html', context)

@login_required(login_url='login_user')
def gallery(request):
    context = {}

    IntruderImage_list = IntruderImage.objects.all()

    # Set the number of items to display per page
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(IntruderImage_list, items_per_page)

    # Get the current page number from the request
    page_number = request.GET.get('page')

    # Get the items for the current page
    page_obj = paginator.get_page(page_number)

    # Pass the paginated data to the template context
    context['page_obj'] = page_obj

    return render(request, 'pages/intrudergallery.html', context)

@login_required(login_url='login_user')
def profile(request):
    context = {}  # Initialize the context dictionary
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        context['form'] = form
        if form.is_valid():
            user = form.save()
            # Ensure the user stays logged in after password change
            update_session_auth_hash(request, user)
            # Redirect to a success page or render a template with a success message
            context['alert_error'] = 'Password Changed'

    elif request.method == 'POST' and 'username' in request.POST:
        try:
            current_user = request.user
            current_user_data = User.objects.get(id=current_user.id)
            current_user_data.username = request.POST['username']

            current_user_data.save()
            context['alert_error'] = 'Edit Success'

            try:
                current_user = current_user_data
                user_image = UserImage.objects.get(userID=current_user)
                context['user_image'] = user_image 
                context['current_user'] = current_user 

            except UserImage.DoesNotExist:
                context['alert_error'] = 'Image does not exist'
            return render(request, 'pages/profile.html', context)
        except IntegrityError:
            context['alert_error'] = 'Username Already Exist'

    elif request.method == 'POST' and len(request.FILES) != 0:
        try:
            current_user = request.user
            user_image = UserImage.objects.get(userID=current_user)
            
            user_image.userImage = request.FILES('image')
            user_image.save()
        except UserImage.DoesNotExist:
           context['alert_error'] = 'Image does not exist'
    
    form = PasswordChangeForm(user=request.user)

    try:
        current_user = request.user
        user_image = UserImage.objects.get(userID=current_user)
        context['user_image'] = user_image 
        context['current_user'] = current_user 
    except UserImage.DoesNotExist:
        context['alert_error'] = 'Image does not exist'

    return render(request, 'pages/profile.html', context)
    