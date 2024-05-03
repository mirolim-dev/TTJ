# serializers.py

from rest_framework import serializers
from .models import Student, Booking

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'gender', 'address', 'phone', 'image', 'university', 'faculty', 'group', 'study_type', 'smena']


class BookingSerializer(serializers.ModelSerializer):
    student = StudentSerializer()  # Include Student data in Booking response

    class Meta:
        model = Booking
        fields = ['student', 'description']
