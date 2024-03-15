from django import forms
from .models import Staff


class StaffForm(forms.ModelForm):
    
    class Meta:
        model = Staff
        fields = ("first_name", 'last_name', 'address', 'phone', 'gender', 'position', 'salary', 'image', 'is_working')
