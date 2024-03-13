from django.contrib import admin

# from local apps
from .admission_models import Admission
from .models import (
    Ttj, Room, Stuff, RoomStuff, Bed, Staff
)
# Register your models here.

class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'room', 'status', 'contract', 'created_at', 'updated_at']
    list_filter = ['status']
    search_fields = ['student__first_name', 'student__last_name', 'room__name']
    list_display_links = ['student']
admin.site.register(Admission, AdmissionAdmin)


class TtjAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'university', 'image', 'location', 'location_link', 'joined_at']
    search_fields = ['name', 'location']
    list_display_links = ['name']
admin.site.register(Ttj, TtjAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttj', 'name']
    search_fields = ['ttj__name', 'name']
admin.site.register(Room, RoomAdmin)


class BedAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttj', 'name', 'capacity', 'status']
    list_filter = ['status']
    search_fields = ['ttj__name', 'name', 'capacity']
admin.site.register(Bed, BedAdmin)


class StuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'amount_of_existance']
    search_fields = ['name']
    list_display_links = ['name']
admin.site.register(Stuff, StuffAdmin)


class RoomStuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'stuff', 'room', 'amount']
    search_fields = ['room__name']
admin.site.register(RoomStuff, RoomStuffAdmin)


class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'address', 'position', 'salary']
    list_filter = ['position']
    search_fields = ['first_name', 'last_name', 'phone']
    list_display_links = ['first_name']
admin.site.register(Staff, StaffAdmin)
