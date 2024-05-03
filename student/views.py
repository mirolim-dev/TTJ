from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Booking
from university.models import Faculty, University
from .models import StudentTracking, Student
from ttj.models import Ttj
from .serializers import BookingSerializer
# Create your views here.


def track_student(request, ttj_id:int, student_id:int):
    ttj = Ttj.objects.get(id=ttj_id)
    student = Student.objects.get(id=student_id)
    device_ip = request.META.get('REMOTE_ADDR', None) #Qr code scanner's IP address
    StudentTracking.objects.create(student=student, ttj=ttj)
    return HttpResponse(f"Device IP: {device_ip}")



    
class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        # Automatically insert Student data when creating a Booking
        first_name = self.request.data.get('student.first_name') 
        last_name = self.request.data.get('student.last_name') 
        gender = self.request.data.get('student.gender') 
        address = self.request.data.get('student.address') 
        phone = self.request.data.get('student.phone') 
        image = self.request.data.get('student.image') 
        university_id = self.request.data.get('student.university') 
        faculty_id = self.request.data.get('student.faculty') 
        group = self.request.data.get('student.group') 
        study_type = self.request.data.get('student.study_type') 
        smena = self.request.data.get('student.smena') 
        description = self.request.data.get('description')
        university = University.objects.get(id=university_id)
        faculty = Faculty.objects.get(id=faculty_id)
        student = Student.objects.create(
            first_name=first_name, last_name=last_name, gender=gender,
            address = address, phone=phone, image=image, university=university,
            faculty=faculty, group=group, study_type=study_type,
            smena=smena
            )
        serializer.save(university=university, student=student, description=description)
