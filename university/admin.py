from django.contrib import admin

# from local apps
from .models import University, Faculty
# Register your models here.


class UnivesityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'location_link', 'joined_at']
    search_fields = ['name', 'location']
admin.site.register(University, UnivesityAdmin)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'university', 'name']
    search_fields = ['university__name', 'name']
admin.site.register(Faculty, FacultyAdmin)