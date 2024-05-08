from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# from .templatetags.custom_filters import get_field
from university.models import Faculty, University
from .forms import StudentBookingForm, LoginForm

# Create your views here.
# @login_required(login_url='sign_in')
def home(request):

    context = {}
    return render(request, 'home.html', context)


def registration(request):
    form = StudentBookingForm()
    if request.POST:
        form = StudentBookingForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            form.save()
            User = get_user_model()
            student_user = User.objects.get(phone=phone)
            student_user.set_password(password)
            student_user.save()

            # Authenticate the student_user
            student_user = authenticate(username=student_user.username, password=password)
            if student_user is not None:
                login(request, student_user)
                return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'register-login/registration.html', context)


def get_faculties(request):
    university_id = request.GET.get('university')
    faculties = Faculty.objects.filter(university__id=university_id)
    context = {
        'faculties': faculties
    }
    return render(request, 'register-login/partials/faculty_options.html', context)

def sign_in(request):
    form = LoginForm()
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            User = get_user_model()
            student_user = User.objects.get(phone=phone)
            student_user = authenticate(username=student_user.username, password=password)
            if student_user is not None:
                login(request, student_user)
                return redirect('home')
    context = {
        'form': form,
    }

    return render(request, 'register-login/login.html', context)


def demo_redirection(request, action:str):
    phone, password = None, None
    if action == "role-reviewer":
        phone = "+998997654321"
        password = "e1g5-}1F"
    elif action == "role-mudir":
        phone = "+998978457654"
        password = "mr011012"
    
    User = get_user_model()
    _user = User.objects.get(phone=phone)
    _user = authenticate(username=_user.username, password=password)
    # print("USer", _user)
    if _user is not None:
        login(request, _user)
        return redirect('/admin/')
    context = {}
    return render(request, 'home.html', context)