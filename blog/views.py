from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import UserModel

from django.shortcuts import render

def home(request):
    return render(request, 'blog/home.html')


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_exists = UserModel.objects.filter(username=username).exists()

        if user_exists:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_msg = 'Invalid password'
        else:
            UserModel.objects.create_user(username=username, password=password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'blog/reg.html')