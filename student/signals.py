from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (
    BlackList, Student
)


@receiver(post_save, sender=BlackList)
def change_student_status_by_black_list(sender, instance, **kwargs):
    student = instance.student
    student.status = 0
    student.save()



