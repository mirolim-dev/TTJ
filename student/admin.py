from django.contrib import admin


# from local apps
from .models import (
    Student, Booking, BlackList, 
    StudentTracking, Payment
    )
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'gender', 'phone', 
        'address', 'university', 'faculty', 
        'group', 'study_type', 'smena', 'status',
        'approved', 'balance'
        ]

    list_editable = [
        'phone', 'address', 'smena', 'status',
    ]
    list_filter = [
        'study_type', 'gender', 'status', 'smena',
    ]
    search_fields = ['first_name', 'last_name', 'phone', 'group']
admin.site.register(Student, StudentAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'student', 'status', 'booked_at', 'updated_at'
    ]
    list_editable = ['status']
    list_filter = ['status']
    search_fields = [
        'student__first_name', 'student__last_name'
    ]
admin.site.register(Booking, BookingAdmin)