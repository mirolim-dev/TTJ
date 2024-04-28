from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group, User  
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phone', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'display_gender')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'gender')
    fieldsets = (
        (None, {'fields': ('phone', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'address', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone', 'username', 'email', 'first_name', 'last_name')
    ordering = ('phone',)

# admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.unregister(Group)
# admin.site.register(Group, GroupAdmin)
