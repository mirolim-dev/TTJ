from django.http import HttpResponse
from django.shortcuts import render
from .models import StudentTracking, Student
from ttj.models import Ttj
# Create your views here.


def track_student(request, ttj_id:int, student_id:int):
    ttj = Ttj.objects.get(id=ttj_id)
    student = Student.objects.get(id=student_id)
    device_ip = request.META.get('REMOTE_ADDR', None) #Qr code scanner's IP address
    StudentTracking.objects.create(student=student, ttj=ttj)
    return HttpResponse(f"Device IP: {device_ip}")