from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['image', 'university', 'faculty', 'group', 'study_type', 'smena', 'status', 'approved', 'balance']
