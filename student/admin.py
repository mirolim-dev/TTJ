from django.contrib import admin

from config.utils import user_group_is_exist
from config.global_variables import UNIVERSITY_STAFF_GROUP, MUDIR_GROUP
# from local apps
from .forms import StudentForm
from .models import (
    Student, Booking,
    BookingReview, BlackList, 
    StudentTracking, Payment
    )
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user_group_is_exist(user, UNIVERSITY_STAFF_GROUP):
            return qs.filter(booking__university = user.bookingreviewer.university)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "booking" and request.user.is_authenticated and user_group_is_exist(request.user, UNIVERSITY_STAFF_GROUP):
            kwargs["queryset"] = Booking.objects.filter(university=request.user.bookingreviewer.university)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
admin.site.register(BookingReview, BookingReviewAdmin)


class BlackListAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'student', 'ttj', 'created_at'
    ]
    search_fields = ['student__first_name', 'student__last_name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(ttj=request.user.staff.ttj) 
        return qs
        
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if user_group_is_exist(request.user, MUDIR_GROUP):
            default_ttj = request.user.staff.ttj
            form.base_fields['ttj'].disabled = True
            form.base_fields['ttj'].initial = default_ttj
        return form

    def save_model(self, request, obj, form, change):
        if not change and user_group_is_exist(request.user, MUDIR_GROUP):  # Only set the university for new objects, not for existing ones
            obj.ttj = request.user.staff.ttj
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if request.user.is_authenticated and user_group_is_exist(user, MUDIR_GROUP):
            if db_field.name == "student":
                kwargs["queryset"] = Student.objects.filter(university=user.staff.ttj.university, approved=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
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