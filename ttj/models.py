from django.db import models
from django.db.models import Count

from account.models import CustomUser
# from locals
from university.models import University
from .validators import (
    validate_changing_bed_status,
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
        return self.admission_set.filter(status=1).aggregate(students_in_ttj=Count('id'))['students_in_ttj']

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
        return f"{self.name} - {self.get_available_places()}"
    
    def clean(self) -> None:
        return super().clean()
    
    def save(self):
        if self.pk:
            validate_changing_bed_status(self)
        return super().save()

    def get_str_status(self)->str:
        return self.STATUS_CHOICES[self.status][1]

class Stuff(models.Model):
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
    image = models.ImageField(upload_to="Staff/Images", blank=True)
    POSITION_CHOICES = (
        (0, "Mudir"),
        (1, "Qorovul"),
        (2, "Hamshira"),
        (3, "Tarbiyachi"),
        (4, "Farrosh"),
    )
    position = models.IntegerField(choices=POSITION_CHOICES, default=2)
    salary = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text="Maoshni UZS da kiriting")
    is_working = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name()} | {self.display_position()}"
    
    def display_position(self):
        return self.POSITION_CHOICES[self.position][1]


