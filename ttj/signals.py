from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from student.models import Student
from .models import Admission
from .utils import generate_qr

@receiver(post_save, sender=Admission)
def update_bed_status_by_admission(sender, instance, **kwargs):
    # if not instance.pk:
    room = instance.room
    if room.get_available_places() == 0:
        room.status = 0
        room.save()
    student = instance.student
    qr_image = generate_qr(student)
    student.qr_code_file = qr_image
    student.save()