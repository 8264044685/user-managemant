from django.shortcuts import render, redirect, Http404
from django.core.mail import send_mail
from django.conf import settings
# from .form import SignUpForm
from .form import SignUpForm, ProfileForm
from django.contrib.auth.models import auth
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profileForm = ProfileForm(request.POST, request.FILES)

        if form.is_valid() and profileForm.is_valid():
            print("success")
            user = form.save()
            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('login')
        else:
            # messages.error(request,'Wrong Input')
            return render(request, 'login/signup.html', {'form': form, 'userProfileForm': profileForm})
    else:
        profileForm = ProfileForm()
        form = SignUpForm()
        # context = {'form': profileForm}
        context = {'form': form, 'userProfileForm': profileForm, }
        return render(request, 'login/signup.html', context)
    return render(request, 'login/signup.html', {'form': form, 'userProfileForm': profileForm})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are login successfully")
            return redirect('welcome')
        else:
            messages.warning(request, "Username and password are not match")
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'login/login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    auth.logout(request)
    return render(request, 'pages/index.html')


def reset_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        admin_email = 'parasdabhi1996@gmail.com'

        if email == None or email == "":
            messages.error(request, email)
            return redirect('reset_password')
        else:
            if User.objects.filter(email=email).exists():
                send_mail(
                    'This mail for reset password',
                    'just Click Below link to reset password',
                    'Thank you for using our services.'
                    'parasdabhi2021@gmail.com',
                    [admin_email, email],
                    fail_silently=False
                )
                messages.success(request, "Check your E-mail to  reset password : " + email)
                return redirect('reset_password')
            else:
                messages.error(request, "Entered email is not match  : " + email)
                return redirect('reset_password')
    else:
        # messages.info(request, "Please enter email")
        return render(request, 'login/reset_password.html')

