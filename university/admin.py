from django.contrib import admin

# from local apps
from config.global_variables import (
    UNIVERSITY_STAFF_GROUP,
)
from config.utils import user_group_is_exist
from .models import University, Faculty, BookingReviewer
from .forms import BookingReviewerForm
# Register your models here.


class UnivesityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'location_link', 'joined_at']
    search_fields = ['name', 'location']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs.exists() & user_group_is_exist(request.user, UNIVERSITY_STAFF_GROUP):
            return qs.filter(id=request.user.bookingreviewer.university.id)
        return qs
admin.site.register(University, UnivesityAdmin)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'university', 'name']
    search_fields = ['university__name', 'name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs.exists() & user_group_is_exist(request.user, UNIVERSITY_STAFF_GROUP):
            return qs.filter(university=request.user.bookingreviewer.university)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if hasattr(request.user, 'bookingreviewer'):
            default_university = request.user.bookingreviewer.university
            form.base_fields['university'].disabled = True
            form.base_fields['university'].initial = default_university
        return form

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the university for new objects, not for existing ones
            if hasattr(request.user, 'bookingreviewer'):
                obj.university = request.user.bookingreviewer.university
        super().save_model(request, obj, form, change)
admin.site.register(Faculty, FacultyAdmin)


class BookingReviewerAdmin(admin.ModelAdmin):
    form = BookingReviewerForm
    list_display = ['id', 'first_name', 'last_name', 'phone', 'salary', 'university', 'is_working']
    list_filter = ['is_working']
    search_fields = ['first_name', 'last_name', 'phone', 'university__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs.exists() & user_group_is_exist(request.user, UNIVERSITY_STAFF_GROUP):
            return qs.filter(university=request.user.bookingreviewer.university)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if hasattr(request.user, 'bookingreviewer'):
            default_university = request.user.bookingreviewer.university
            form.base_fields['university'].disabled = True
            form.base_fields['university'].initial = default_university
        return form

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the university for new objects, not for existing ones
            if hasattr(request.user, 'bookingreviewer'):
                obj.university = request.user.bookingreviewer.university
        super().save_model(request, obj, form, change)
admin.site.register(BookingReviewer, BookingReviewerAdmin)
