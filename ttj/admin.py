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
            return qs.filter(room__ttj=request.user.staff.ttj) 
        return qs
admin.site.register(Admission, AdmissionAdmin)


class TtjAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'university', 'image', 'location', 'location_link', 'joined_at']
    search_fields = ['name', 'location']
    list_display_links = ['name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(id=request.user.staff.ttj.id) 
        elif user_group_is_exist(request.user, UNIVERSITY_STAFF_GROUP) & qs.exists():
            return qs.filter(university=request.user.bookingreviewer.university)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if hasattr(request.user, 'bookingreviewer') & user_group_is_exist(request.user, UNIVERSITY_STAFF_GROUP):
            default_university = request.user.bookingreviewer.university
            form.base_fields['university'].disabled = True
            form.base_fields['university'].initial = default_university
        return form

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the university for new objects, not for existing ones
            if hasattr(request.user, 'bookingreviewer'):
                obj.university = request.user.bookingreviewer.university
        super().save_model(request, obj, form, change)
admin.site.register(Ttj, TtjAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttj', 'name']
    search_fields = ['ttj__name', 'name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(ttj=request.user.staff.ttj) 
        return qs
admin.site.register(Room, RoomAdmin)


class BedAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttj', 'name', 'capacity', 'status']
    list_filter = ['status']
    search_fields = ['ttj__name', 'name', 'capacity']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(ttj=request.user.staff.ttj)
        return qs
admin.site.register(Bed, BedAdmin)


class StuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'amount_of_existance']
    search_fields = ['name']
    list_display_links = ['name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(ttj=request.user.staff.ttj) 
        return qs
admin.site.register(Stuff, StuffAdmin)


class RoomStuffAdmin(admin.ModelAdmin):
    list_display = ['id', 'stuff', 'room', 'amount']
    search_fields = ['room__name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(room__ttj=request.user.staff.ttj)
        return qs
admin.site.register(RoomStuff, RoomStuffAdmin)


class StaffAdmin(admin.ModelAdmin):
    form = StaffForm
    list_display = ['id', 'first_name', 'last_name', 'phone', 'address', 'ttj', 'position', 'salary', 'is_working']
    list_filter = ['position']
    search_fields = ['first_name', 'last_name', 'phone']
    list_display_links = ['first_name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if user_group_is_exist(request.user, MUDIR_GROUP) & qs.exists():
            return qs.filter(ttj=request.user.staff.ttj) 
        elif user_group_is_exist(request.user, UNIVERSITY_STAFF_GROUP):
            print("Booking Reviewer here")
            return qs.filter(ttj__university=request.user.bookingreviewer.university, position__in=[0, 3])
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if user_group_is_exist(request.user, MUDIR_GROUP):
            default_ttj = request.user.staff.ttj
            form.base_fields['ttj'].disabled = True
            form.base_fields['ttj'].initial = default_ttj
        return form
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ttj" and request.user.is_authenticated and user_group_is_exist(request.user, UNIVERSITY_STAFF_GROUP):
            kwargs["queryset"] = Ttj.objects.filter(university=request.user.bookingreviewer.university)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "position" and request.user.is_authenticated:
            if user_group_is_exist(request.user, UNIVERSITY_STAFF_GROUP):
                # Limit the choices for Booking Reviewers
                kwargs["choices"] = [
                    choice for choice in Staff.POSITION_CHOICES 
                    if choice[0] in [0, 3]  # Only allow Mudir (0) and Tarbiyachi (3)
                ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the university for new objects, not for existing ones
            if user_group_is_exist(request.user, MUDIR_GROUP):
                obj.ttj = request.user.staff.ttj
        super().save_model(request, obj, form, change)
admin.site.register(Staff, StaffAdmin)
