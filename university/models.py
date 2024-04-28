from django.db import models
from account.models import CustomUser
from config.utils import generate_password
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


class BookingReviewer(CustomUser):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    is_working = models.BooleanField(default=True)
    visible_password = models.CharField(max_length=150, verbose_name="PassWord", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.visible_password:
            self.visible_password = generate_password(8)
        try:
            self.set_password(self.visible_password)
        except:
            pass
        self.is_staff = True
        return super().save(*args, **kwargs) 