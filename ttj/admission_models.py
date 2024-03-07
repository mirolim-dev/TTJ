from django.db import models

# from local
from student.models import Student

class Admission(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="Ttj/Admission")
    location = models.CharField(max_length=250)
    location_link = models.CharField(max_length=250)
    joined_at = models.DateTimeField(auto_now_add=True)

    def get_all_ttj(self):
        pass

    def get_all_students_in_ttj(self):
        pass

    def __str__(self) -> str:
        return self.name
    

    class Meta:
        ordering = ['-joined_at']