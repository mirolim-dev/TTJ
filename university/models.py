from django.db import models
from account.models import CustomUser
from config.utils import generate_password
# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name="Nomi")
    image = models.ImageField(upload_to='university')
    location = models.CharField(max_length=250, verbose_name="Manzili")
    location_link = models.CharField(max_length=250, blank=True, verbose_name="Mazil uchun link")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Dasturga qo'shilgan vaqti")

    class Meta:
        ordering = ['-joined_at']
        verbose_name_plural = "Universitet"

    def __str__(self):
        return self.name
    
    def get_all_ttj(self):
        return self.ttj_set.select_related('university')


    def get_all_students_placed_in_ttj(self):
        return self.ttj.get_all_student_int_ttj()

    

class Faculty(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name="Universitet")
    name = models.CharField(max_length=250, verbose_name="Nomi")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Fakultetlar"


class BookingReviewer(CustomUser):
    class Meta:
        verbose_name_plural = "So'rovlarni ko'ruvchi shaxs"
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name="Universitet")
    salary = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name="Maosh")
    is_working = models.BooleanField(default=True, verbose_name="Ishlayotganlik statusi")
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