from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

from student.models import Student
from account.permissions import ttj_mudir_permissions
from .models import Admission, Staff
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


@receiver(post_save, sender=Staff)
def give_permission_group_to_staff(sender, instance, **kwargs):
    group_name = "TTJ Mudiri" 
    """positions of staff:
        POSITION_CHOICES = (
        (0, "Mudir"),
        (1, "Qorovul"),
        (2, "Hamshira"),
        (3, "Tarbiyachi"),
        (4, "Farrosh"),
    )
    """
    if instance.position == 0:
        try:
            group = Group.objects.get(name=group_name)
        except:
            group = Group.objects.create(name=group_name)
            permissions = Permission.objects.filter(codename__in=ttj_mudir_permissions)
            group.permissions.add(*permissions)
            group.save()
        instance.groups.add(group)
    