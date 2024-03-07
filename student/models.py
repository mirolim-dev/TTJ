from django.db import models

# from locals
from account.models import CustomUser
from university.models import Faculty, University
from ttj.models import Ttj
# Create your models here.

class Student(CustomUser):
    image = models.ImageField(upload_to="Studen/Image", blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    group = models.CharField(max_length=50)
    STUDY_CHOICES = (
        (0, "Sirtqi"),
        (1, "Ananaviy")
    )
    study_type = models.IntegerField(choices=STUDY_CHOICES, default=1)
    SMENA_CHOICES = (
        (0, "1-smena"),
        (1, "2-smena"),
        (2, "Kechgi smena")
    )
    smena = models.IntegerField(choices=SMENA_CHOICES, default=0)
    STATUS_CHOICES = (
        (0, "Qora Ro'yxatda"),
        (1, '1-guruh nogironi'),
        (2, "Yoshlar dafarida turadi"),
        (3, 'Chin yetim'),
    )
    status = models.IntegerField(STATUS_CHOICES, blank=True, null=True)
    approved = models.BooleanField(default=False) #TTJ ga qabul qilingan yoki qilnamaganlik statusi
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True)
    qr_code_data = models.CharField(max_length=150, blank=True, null=True)
    qr_code_file = models.ImageField(upload_to="Student/Qr_code")

    def __str__(self):
        return f"{self.get_full_name} | {self.group}"


    class Meta:
        verbose_name_plural = ['Students']
        ordering = ['date_joined']

    def get_all_payments(self):
        pass


class Booking(models.Model):
    class Meta:
        ordering = ['-booked_at']
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    BOOKING_STATUS_CHOICES = (
        (0, "TTJ ga joylashtirish so'rovi rad etildi"),
        (1, "Ko'rib chiqilmoqda"),
        (2, "TTJ ga qabul qilindi"),
    )
    status = models.IntegerField()
    description = models.TextField()
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def display_status_data(self):
        return self.BOOKING_STATUS_CHOICES[self.status][1]    

    def __str__(self):
        return f"{self.student.get_full_name()} | {self.display_status_data()}"

    
class BlackList(models.Model):
    class Meta:
        ordering = ['created_at']
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ttj = models.ForeignKey(Ttj, on_delete=models.CASCADE) #waiting for TJJ model is been created
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def  __str__(self):
        return self.student.get_full_name() + self.ttj.name


class StudentTracking(models.Model):
    class Meta:
        ordering = ['-tracked_at']
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ttj = models.ForeignKey(Ttj, on_delete=models.CASCADE)
    TRACKING_STATUS = (
        (0, "Chiqdi"),
        (1, "Kirdi"),
    )
    status = models.IntegerField(choices=TRACKING_STATUS, default=1)
    tracked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.get_full_name} | {self.ttj.name} | {self.display_status()} | {self.tracked_at}"

    def display_status(self):
        return self.TRACKING_STATUS[self.status][1]
