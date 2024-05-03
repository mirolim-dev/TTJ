from django.shortcuts import render
from django.contrib.auth import login, authenticate

from student.models import Booking
from student.student_model import Student

# Create your views here.

def registration(request):
    return render(request, 'register-login/registration.html')


def sign_in(request):
    return render(request, 'register-login/login.html')