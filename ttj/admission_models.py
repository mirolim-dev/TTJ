from django.db import models

# from local
from .models import Bed, Ttj

from student.models import Student

class Admission(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    room = models.ForeignKey(Bed, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        (0, "Bekor qilingan"),
        (1, "Active")
    )
    description = models.TextField()
    contract = models.ImageField(upload_to="ttj/contract")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_all_ttj(self):
        pass

    def get_all_students_in_ttj(self):
        pass

    def __str__(self) -> str:
        return self.name
    

    class Meta:
        ordering = ['-created_at']