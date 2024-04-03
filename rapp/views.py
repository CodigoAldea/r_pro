from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from rapp.models import Questions, quesA


# Create your views here.
def home(request):
    return render(request, 'home.html')

# questions and next questions , ocv logic for the video also has to save , 
@login
def depressionque(request):
    que = quesA.objects.all() # all the questions from the db to django
    if request.method == 'POST':
        ques = request.POST.get('ques')
        option = request.POST.get('option')
        
        if option == quesA.objects.get(que = ques).option1 :
            w = 0
        elif option == quesA.objects.get(que = ques).option2 :
            w = 1
        elif option == quesA.objects.get(que = ques).option3 :
            w = 2
        elif option == quesA.objects.get(que = ques).option4 :
            w = 3
        else:
            pass
        
        s = Questions.objects.create(user=login_user, questions=ques, option_text=option, weight=w) 
        # pass the data to the AI Model
        
        return redirect('result')
        
    return render(request, 'depressionque.html', {'que':que})

#score, most common emotion(images) from the video, (lifestyle change (text), information, causes ) : link
def result(request):
    # call the AI model and get the depression_score
    # Logic for calculating depression score and displaying 
    depression_score = 0
    if 0 < depression_score <= 25:
        context = {'depression_score': depression_score, 'severity': 'No depression'}
    elif 25 < depression_score <= 50:
        context = {'depression_score': depression_score, 'severity': 'Mild depression'}
    elif 50 < depression_score <= 75:
        context = {'depression_score': depression_score, 'severity': 'Moderate depression'}
    elif 75 < depression_score <= 100:
        context = {'depression_score': depression_score, 'severity': 'Severe depression'}
    elif 100 < depression_score <= 125:
        context = {'depression_score': depression_score, 'severity': 'Extreme depression'}
    else:
        context = {'depression_score': depression_score, 'severity': 'Unknown severity'}
            
    return render(request, 'result.html', context)

# all the videos in line 
def calming_video(request):
    return render(request, 'calming_video.html')


# only faq
def faq(request):
    return render(request, 'faq.html')

# about
def about_us(request):
    return render(request, 'about_us.html')

def causes(request):
    # Logic for handling causes page
    return render(request, 'causes.html')

# lifestyle changes on result 
def lifestyle_changes(request):
    return render(request, 'lifestyle_changes.html')

# general information on result 
def information(request):
    return render(request, 'information.html')


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
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if name and email and mobile and username and password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, first_name=name)
                user.save()
                user = authenticate(username=username, password= password1)
                login(request, user)
                messages.success(request, ("Registration Successful, you have been Loged in !!!"))
                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
            
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect('home')