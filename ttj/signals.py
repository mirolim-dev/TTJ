from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .admission_models import Admission


@receiver(post_save, sender=Admission)
def update_bed_status_by_admission(sender, instance, **kwargs):
    if not instance.pk:
        instance.save()
        room = instance.room
        if room.get_available_places() == 0:
            room.status = 0
            room.save()
