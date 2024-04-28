from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

from .models import BookingReviewer
from account.permissions import booking_reviewer_permissions


@receiver(post_save, sender=BookingReviewer)
def add_reviewer_to_group(sender, instance, **kwargs):
    group_name = "Universitet xodimi" 
    try:
        group = Group.objects.get(name=group_name)
        print(f"Signal is working while creating booking reviewer")
    except:
        print("Group is not exist")
        group = Group.objects.create(name=group_name)
        permissions = Permission.objects.filter(codename__in=booking_reviewer_permissions)
        group.permissions.add(*permissions)
        group.save()
        print("Group has been created")
    
    instance.groups.add(group)