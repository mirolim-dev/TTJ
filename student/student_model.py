from django.db import models

# from locals
from account.models import CustomUser
from university.models import Faculty, University


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
    smena = models.IntegerField(choices=SMENA_CHOICES, blank=True)
    STATUS_CHOICES = (
        (0, "Qora Ro'yxatda"),
        (1, "1-guruh nogironi"),
        (2, "Yoshlar dafarida turadi"),
        (3, "Chin yetim")
    )
    status = models.IntegerField(choices=STATUS_CHOICES, blank=True, null=True)
    approved = models.BooleanField(default=False) #TTJ ga qabul qilingan yoki qilnamaganlik statusi
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True)
    qr_code_data = models.CharField(max_length=150, blank=True, null=True)
    qr_code_file = models.ImageField(upload_to="Student/Qr_code")

    def __str__(self):
        return f"{self.get_full_name()} | {self.group}"


    class Meta:
        verbose_name_plural = 'Studentlar'
        ordering = ['date_joined']

    def get_all_payments(self):
        pass
