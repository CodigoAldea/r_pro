from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html')

def depressionque(request):
    return render(request, 'depressionque.html')

def faq(request):
    return render(request, 'faq.html')

def about_us(request):
    return render(request, 'about_us.html')

def symptoms(request):
    # Logic for handling symptoms page
    return render(request, 'symptoms.html')

def causes(request):
    # Logic for handling causes page
    return render(request, 'causes.html')

def lifestyle_changes(request):
    return render(request, 'lifestyle_changes.html')

def information(request):
    return render(request, 'information.html')

def calming_video(request):
    return render(request, 'calming_video.html')

def result(request):
    # Logic for calculating depression score and displaying result
    return render(request, 'result.html')


def login_user(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,('Login Successful !!!'))
            return redirect('index')
        else:
            messages.success(request,('Login UN-Successful !!!'))
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def register_user(request):
    return render(request, 'register.html')

def logout_user(request):
    return render(request, 'login.html')