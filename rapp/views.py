from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from rapp.models import Questions, Answer
from .forms import DynamicQuestionForm

import joblib


def load_model():
    try:
        with open('path/to/your/model.joblib', 'rb') as f:
            model = joblib.load(f)
        return model
    except FileNotFoundError:
        raise Exception('Model file not found. Please ensure the model exists.')
# Create your views here.
def calculate_depression_score(x):
    pass
def home(request):
    return render(request, 'home.html')

# questions and next questions , ocv logic for the video also has to save , 
# @login
def depressionque(request):
    all_questions = Questions.objects.all().order_by('id')

    if request.method == 'POST':
        current_question_num = int(request.POST.get('current_question')) + 1
        next_questions = all_questions.filter(id__gt=current_question_num)

        form = DynamicQuestionForm(request.POST, questions=all_questions[:current_question_num])
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for question_id, answer in cleaned_data.items():
                if question_id != 'current_question':
                    question = Questions.objects.get(pk=int(question_id.split('_')[1]))
                    weight = 0 if answer == question.option1 else 1 if answer == question.option2 else 2 if answer == question.option3 else 3
                    Answer.objects.create(question=question, user=login_user, option_text=answer, weight=weight)  # Replace login_user with your authentication mechanism

            if not next_questions:
                return redirect('result')  # Pass all answers to AI model here
            return redirect('depressionque',question_num=current_question_num)
    else:
        if not all_questions:
            # Handle the case where there are no questions
            return render(request, 'depressionque.html', {'message': 'No questions available'})
        form = DynamicQuestionForm(questions=[all_questions[0]])
        question_num = 1

    context = {'form': form, 'question_num': question_num}
    return render(request, 'depressionque.html', context)

#score, most common emotion(images) from the video, (lifestyle change (text), information, causes ) : link
def result(request):
    total_weight = sum(answer.weight for answer in Answer.objects.filter(user=request.user))
                # Pass total_weight to your logic for calculating depression score (replace with your implementation)
    depression_score = calculate_depression_score(total_weight)
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