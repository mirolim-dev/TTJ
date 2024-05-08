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
    university = models.ForeignKey(University,on_delete=models.CASCADE, verbose_name="universitet")
    name = models.CharField(max_length=250,unique=True, verbose_name="Nomi")
    capacity = models.PositiveBigIntegerField(default=0, verbose_name="Sig'imi")
    image = models.ImageField(upload_to='Ttj/Images')
    location = models.CharField(max_length=250, verbose_name="Manzili")
    location_link = models.CharField(max_length=250, verbose_name="Manzil uchun link")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Dasturga qo'shilgan vaqti")

    def get_all_students_in_ttj(self):
        beds = self.room_set.select_related('ttj')

        return Admission.objects.filter(
            Q(room__in=beds) & Q(status=1)
        ).values('student')

    def __str__(self) -> str:
        return self.name
    
    
    class Meta:
        ordering = ['-joined_at']
        verbose_name_plural = "TTJ lar"


class Room(models.Model):
    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"

    ttj = models.ForeignKey(Ttj,on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name="Nomi")

    def __str__(self) -> str:
        return self.name
    

class Bed(Room):
    class Meta:
        verbose_name = "Yotoq"
        verbose_name_plural = "Yotoqlar"

    capacity = models.IntegerField(default=4, verbose_name="Sig'imi")
    STATUS_CHOICES = (
        (0, "Joy qolmagan"),
        (1, "Foydalanishga berilmagan"),
        (2, "Bo'sh"),
        (3, "Bo'sh joylar bor"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, blank=True, null=True, default=2, verbose_name="Xolati")
    
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
    class Meta:
        verbose_name = "Jihoz"
        verbose_name_plural = "Jihozlar"
    ttj = models.ForeignKey(Ttj, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, verbose_name="Nomi")
    image = models.ImageField(upload_to="Ttj/stuff")
    amount_of_existance = models.IntegerField(default=0, verbose_name="Mavjud miqdori")
    description = models.TextField(blank=True, null=True, verbose_name="Izoh")

    def __str__(self) -> str:
        return self.name


class RoomStuff(models.Model):
    class Meta:
        verbose_name_plural = "Xona Jihozlari"
    stuff = models.ForeignKey(Stuff,on_delete=models.CASCADE, verbose_name="Jihoz")
    room = models.ForeignKey(Room,on_delete=models.CASCADE, verbose_name="Xona")
    amount = models.IntegerField(verbose_name="Miqdor")

    def __str__(self) -> str:
        return f"{self.room.name} | {self.stuff.name}"
    

class Staff(CustomUser):
    class Meta:
        ordering = ['first_name', 'date_joined']
        verbose_name_plural = "Xodimlar"
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
    position = models.IntegerField(choices=POSITION_CHOICES, default=2, verbose_name="Pozitisyasi")
    salary = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name="Maosh", help_text="Maoshni UZS da kiriting")
    is_working = models.BooleanField(default=True, verbose_name="Ishlayabdi")

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
        verbose_name_plural = "Tayinlovlar"
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Bed, on_delete=models.CASCADE, verbose_name="Xona")
    STATUS_CHOICES = (
        (0, "Bekor qilingan"),
        (1, "Active")
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Xolati")
    description = models.TextField(verbose_name="Izoh")
    contract = models.ImageField(upload_to="ttj/contract", verbose_name="Shartnoma")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")

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