from django.contrib import admin


# from local apps
from .models import (
    Student, Booking,
    BookingReview, BlackList, 
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


class BookingReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'acceptance', 'last_review_time']
    search_fields = [
        'id',
        'booking__student__first_name', 'booking__student__last_name',
        ]
    list_filter = ['acceptance']
admin.site.register(BookingReview, BookingReviewAdmin)


class BlackListAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'student', 'ttj', 'created_at'
    ]
    search_fields = ['student__first_name', 'student__last_name']
admin.site.register(BlackList, BlackListAdmin)


class StudentTrackingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'student', 'ttj', 'status', 'tracked_at'
    ]
    list_filter = ['status']
    search_fields = ['student__first_name', 'student__last_name']
admin.site.register(StudentTracking, StudentTrackingAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'amount', 'created_at']
    search_fields = ['id', 'student__first_name', 'student__last_name']
admin.site.register(Payment, PaymentAdmin)