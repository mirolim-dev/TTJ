from django.db import models

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='university')
    location = models.CharField(max_length=250)
    location_link = models.CharField(max_length=250, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-joined_at']

    def __str__(self):
        return self.name
    
    def get_all_ttj(self):
        return self.ttj_set.select_related('university')


    def get_all_students_placed_in_ttj(self):
        return self.ttj.get_all_student_int_ttj()

    

class Faculty(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

