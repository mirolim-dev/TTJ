from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

from .models import BookingReviewer
from account.permissions import booking_reviewer_permissions


@receiver(post_save, sender=BookingReviewer)
def add_reviewer_to_group(sender, instance, **kwargs):
    group = Group.objects.get(name="Universitet xodimi")
    print(f"Signal is working while creating booking reviewer")
    if not group:
        print("Group is not exist")
        group = Group.objects.create(name="Universitet xodimi")
        permissions = Permission.objects.filter(codename__in=booking_reviewer_permissions)
        group.permissons.add(*permissions)
        group.save()
        print("Group has been created")
    
    instance.groups.add(group)