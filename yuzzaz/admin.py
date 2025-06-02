from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Custom actions
@admin.action(description='Activate selected users')
def activate_selected_users(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} user(s) activated.", messages.SUCCESS)

@admin.action(description='Deactivate selected users')
def deactivate_selected_users(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"{updated} user(s) deactivated.", messages.WARNING)

# Admin for CustomUser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'is_active', 'email', 'is_staff']
    list_filter = ['is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    actions = [activate_selected_users, deactivate_selected_users]  # <- Add actions here

    fieldsets = (
        (None, {'fields': ('username', 'password')}), 
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'telephone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'first_name', 'last_name',
                'email', 'telephone', 'is_active', 'is_staff',
            ),
        }),
    )

# Register CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)
