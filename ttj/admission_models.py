from django.db import models

# from local
from .models import Bed, Ttj
from .validators import (
    validate_admission_by_bed_status,
    validate_admission_by_student_approvement,
    validate_admission_by_ttj_capacity,
)
from student.models import Student

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
        return self.name
    
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