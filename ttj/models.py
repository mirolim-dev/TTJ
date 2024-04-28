from django.db import models
from django.db.models import Count, Sum, Q

from account.models import CustomUser
from config.utils import generate_password
# from locals
from university.models import University
from student.student_model import Student
from .validators import (
    validate_changing_bed_status,
    validate_admission_by_bed_status,
    validate_admission_by_student_approvement,
    validate_admission_by_ttj_capacity,
)



# from student.models import Student



class Ttj(models.Model):
    university = models.ForeignKey(University,on_delete=models.CASCADE)
    name = models.CharField(max_length=250,unique=True)
    capacity = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to='Ttj/Images')
    location = models.CharField(max_length=250)
    location_link = models.CharField(max_length=250)
    joined_at = models.DateTimeField(auto_now_add=True)

    def get_all_students_in_ttj(self):
        beds = self.room_set.select_related('ttj')

        return Admission.objects.filter(
            Q(room__in=beds) & Q(status=1)
        ).values('student')

    def __str__(self) -> str:
        return self.name
    
    
    class Meta:
        ordering = ['-joined_at']


class Room(models.Model):
    ttj = models.ForeignKey(Ttj,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name
    

class Bed(Room):
    capacity = models.IntegerField(default=4)
    STATUS_CHOICES = (
        (0, "Joy qolmagan"),
        (1, "Foydalanishga berilmagan"),
        (2, "Bo'sh"),
        (3, "Bo'sh joylar bor"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, blank=True, null=True, default=2)
    
    def get_available_places(self):
        # return self.admission_set.filter(status=1).count()
        return self.capacity - self.admission_set.filter(status=1).aggregate(available_places=Count('id'))['available_places'] #dabase hajmi kattalashib ketishligi mumkun bo'lgani uchun ushbu versiya afzal ko'riladi.

    def __str__(self) -> str:
        return f"{self.name} | {self.capacity} - {self.get_available_places()}"
    
    def clean(self) -> None:
        return super().clean()
    
    def save(self):
        if self.pk:
            validate_changing_bed_status(self)
        return super().save()

    def get_str_status(self)->str:
        return self.STATUS_CHOICES[self.status][1]

    def get_number_of_active_admissions(self):
        return self.admission_set.filter(status=1).aggregate(active_admissions=Count('id'))['active_admissions']


class Stuff(models.Model):
    ttj = models.ForeignKey(Ttj, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="Ttj/stuff")
    amount_of_existance = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class RoomStuff(models.Model):
    stuff = models.ForeignKey(Stuff,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.room.name} | {self.stuff.name}"
    

class Staff(CustomUser):
    class Meta:
        ordering = ['first_name', 'date_joined']
    ttj = models.ForeignKey(Ttj, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="Staff/Images", blank=True)
    POSITION_CHOICES = (
        (0, "Mudir"),
        (1, "Qorovul"),
        (2, "Hamshira"),
        (3, "Tarbiyachi"),
        (4, "Farrosh"),
    )
    visible_password = models.CharField(max_length=150, verbose_name="PassWord", null=True, blank=True)
    position = models.IntegerField(choices=POSITION_CHOICES, default=2)
    salary = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text="Maoshni UZS da kiriting")
    is_working = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name()} | {self.display_position()}"

    def save(self, *args, **kwargs):
        if not self.visible_password:
            self.visible_password = generate_password(8)
        try:
            self.set_password(self.visible_password)
        except:
            pass
        self.is_staff = True
        return super().save(*args, **kwargs) 
    def display_position(self):
        return self.POSITION_CHOICES[self.position][1]


class Admission(models.Model):
    class Meta:
        ordering = ['-created_at']
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    room = models.ForeignKey(Bed, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        (0, "Bekor qilingan"),
        (1, "Active")
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    description = models.TextField()
    contract = models.ImageField(upload_to="ttj/contract")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.student} | {self.room} | {self.display_status()}"
    
    def clean(self) -> None:
        validate_admission_by_bed_status(self.room.status)
        validate_admission_by_student_approvement(self.student)
        validate_admission_by_ttj_capacity(self.room.ttj)
        return super().clean()
    
    def save(self):
        if self.pk and self.status == 0 :
            if self.room.get_available_places() == self.room.capacity:
                self.room.status = 2
            else:
                self.room.status = 3
            self.room.save()
        return super().save()

    def display_status(self):
        return self.STATUS_CHOICES[self.status][1]

    @property
    def get_ttj(self):
        return self.room.ttj