from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (
    BlackList, Student, Booking, BookingReview
)


@receiver(post_save, sender=BlackList)
def change_student_status_by_black_list(sender, instance, **kwargs):
    student = instance.student
    student.status = 0
    student.save()


@receiver(post_save, sender=Booking)
def change_student_approved_field_by_booking(sender, instance, **kwargs):
    if instance.status == 2:
        student = instance.student
        student.approved = True
        student.save()

    

@receiver(post_save, sender=BookingReview)
def update_booking_sattus_by_bookin_review(sender, instance, **kwargs):
    booking = instance.booking
    if instance.acceptance == 1:
        booking.status = 2
    else:
        booking.status = 0
    booking.save()

