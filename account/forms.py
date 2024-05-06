from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate, login

from student.models import Booking
from student.student_model import Student
from university.models import University, Faculty
    
class StudentBookingForm(forms.Form):
    first_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+9989999999'. Up to 15 digits allowed."
    )
    phone = forms.CharField(validators=[phone_regex], max_length=17, required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone'})    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    GENDER_CHOICES = (
        (0, "Female"),
        (1, "Male")
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, initial=1, widget=forms.Select(attrs={'placeholder': 'Gender'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'placeholder': 'Image'}))
    university = forms.ModelChoiceField(queryset=University.objects.all(), widget=forms.Select(attrs={"hx-get": "get_faculties", "hx-target": "#id_faculty"}))
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.none(), widget=forms.Select(attrs={'placeholder': 'Faculty'}))
    group = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Group'}))
    STUDY_CHOICES = (
        (0, "Sirtqi"),
        (1, "Ananaviy")
    )
    study_type = forms.ChoiceField(choices=STUDY_CHOICES, initial=1, widget=forms.Select(attrs={'placeholder': 'Study Type'}))
    SMENA_CHOICES = (
        (0, "1-smena"),
        (1, "2-smena"),
        (2, "Kechgi smena")
    )
    smena = forms.ChoiceField(choices=SMENA_CHOICES, initial=0, widget=forms.Select(attrs={'placeholder': 'Smena'}))
    STATUS_CHOICES = (
        (1, "1-guruh nogironi"),
        (2, "Yoshlar dafarida turadi"),
        (3, "Chin yetim"),
        (4, "Mavjud emas"),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Ijtimoiy ustunligi', widget=forms.Select(attrs={'placeholder': 'Ijtimoiy ustunligi'}), initial=4)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description'}), initial="Default description")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        if "university" in self.data:
            university_id = int(self.data.get('university'))
            self.fields['faculty'].queryset = Faculty.objects.filter(university__id=university_id)

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationErr("Passwords do not match.")
        super().clean()

    def save(self, commit=True):
        # Extract data for each model


        university_instance = self.cleaned_data.get('university')
        faculty_instance = self.cleaned_data.get('faculty')

        # Get University and Faculty instances
        # university_instance = University.objects.get(pk=university_id)
        # faculty_instance = Faculty.objects.get(pk=faculty_id)
        student_data = {
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'address': self.cleaned_data['address'],
            'phone': self.cleaned_data['phone'],
            # 'email':self.cleaned_data['email'],
            'gender': self.cleaned_data['gender'],
            'image': self.cleaned_data['image'],
            'university': university_instance,
            'faculty': faculty_instance,
            'group': self.cleaned_data['group'],
            'study_type': self.cleaned_data['study_type'],
            'smena': self.cleaned_data['smena'],
            # Other student fields...
        }
        if self.cleaned_data.get('status') != 4:
            student_data['status'] = self.cleaned_data.get('status')
        student = Student.objects.create(**student_data)

        booking_data = {
            'university': university_instance,
            'student': student, 
            'description': self.cleaned_data['description'],
        }
        booking = Booking.objects.create(**booking_data)


class LoginForm(forms.Form):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+9989999999'. Up to 15 digits allowed."
    )
    phone = forms.CharField(validators=[phone_regex], max_length=17, required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})