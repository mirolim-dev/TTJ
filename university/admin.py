from django.contrib import admin

# from local apps
from .models import University, Faculty, BookingReviewer
from .forms import BookingReviewerForm
# Register your models here.


class UnivesityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'location_link', 'joined_at']
    search_fields = ['name', 'location']
admin.site.register(University, UnivesityAdmin)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'university', 'name']
    search_fields = ['university__name', 'name']
admin.site.register(Faculty, FacultyAdmin)


class BookingReviewerAdmin(admin.ModelAdmin):
    form = BookingReviewerForm
    list_display = ['id', 'first_name', 'last_name', 'phone', 'salary', 'university', 'is_working']
    list_filter = ['is_working']
    search_fields = ['first_name', 'last_name', 'phone', 'university__name']
admin.site.register(BookingReviewer, BookingReviewerAdmin)
