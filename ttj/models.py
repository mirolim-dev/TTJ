from django.db import models

# from locals
from university.models import University
# from student.models import Student



class Ttj(models.Model):
    university = models.ForeignKey(University,on_delete=models.CASCADE)
    name = models.CharField(max_length=250,unique=True)
    image = models.ImageField(upload_to='Ttj/Images')
    location = models.CharField(max_length=250)
    location_link = models.CharField(max_length=250)
    joined_at = models.DateTimeField(auto_now_add=True)

    def get_all_student_in_ttj(self):
        pass

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
    status = models.IntegerField(STATUS_CHOICES, blank=True, null=True)
    
    def get_available_places(self):
        pass

    def __str__(self) -> str:
        return f"{self.name} - {self.get_available_places()}"
    

class Stuff(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="Ttj/staff")
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
    

