from django.contrib import admin

# from local apps
from .models import (
    Ttj, Room, Stuff, RoomStuff, Bed, Staff, 
    Admission,
)
from config.global_variables import (
    MUDIR_GROUP, UNIVERSITY_STAFF_GROUP,
)
from config.utils import user_group_is_exist

from .forms import StaffForm
# Register your models here.


class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'room', 'status', 'contract', 'created_at', 'updated_at']
    list_filter = ['status']
    search_fields = ['student__first_name', 'student__last_name', 'room__name']
    list_display_links = ['student']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(room__ttj=request.user.staff_set.first().ttj) 
        return qs
admin.site.register(Admission, AdmissionAdmin)


class TtjAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'university', 'image', 'location', 'location_link', 'joined_at']
    search_fields = ['name', 'location']
    list_display_links = ['name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(qs)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(id=request.user.staff_set.first().ttj.id) 
        elif user_group_is_exist(request.user, UNIVERSITY_STAFF_GROUP) & qs.exists():
            return qs.filter(university=request.user.bookingreviewer.university)
        return qs
admin.site.register(Ttj, TtjAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttj', 'name']
    search_fields = ['ttj__name', 'name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(ttj=request.user.staff_set.first().ttj) 
        return qs
admin.site.register(Room, RoomAdmin)


class BedAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttj', 'name', 'capacity', 'status']
    list_filter = ['status']
    search_fields = ['ttj__name', 'name', 'capacity']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(ttj=request.user.staff_set.first().ttj)
        return qs
admin.site.register(Bed, BedAdmin)


class StuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'amount_of_existance']
    search_fields = ['name']
    list_display_links = ['name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(ttj=request.user.staff_set.first().ttj) 
        return qs
admin.site.register(Stuff, StuffAdmin)


class RoomStuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'stuff', 'room', 'amount']
    search_fields = ['room__name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(room__ttj=request.user.staff_set.first().ttj)
        return qs
admin.site.register(RoomStuff, RoomStuffAdmin)


class StaffAdmin(admin.ModelAdmin):
    form = StaffForm
    list_display = ['id', 'first_name', 'last_name', 'phone', 'address', 'position', 'salary', 'is_working']
    list_filter = ['position']
    search_fields = ['first_name', 'last_name', 'phone']
    list_display_links = ['first_name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(ttj=request.user.staff_set.first().ttj) 
        return qs
admin.site.register(Staff, StaffAdmin)
