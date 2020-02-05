from django.shortcuts import render
from login.models import userProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from comments.models import post, like
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'pages/index.html')


# welcome method like Dashboard
@login_required(login_url='/login/login')
def welcome(request):
    user_id = request.user.id
    posts = post.objects.select_related('user', )
    context = {'posts': posts, 'user_id': user_id}
    return render(request, 'pages/welcome.html', context)


# show all the User data
@login_required(login_url='/login/login')
def show_data(request):
    users = User.objects.all().select_related('userprofile')
    print(users.query)
    context = {
        'userData': users,
    }
    return render(request, 'pages/show_data.html', context)
