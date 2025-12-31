from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'email',  # show email first
        'username',
        'first_name',
        'last_name',
        'phone',
        'status',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'status',
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # use email instead of username

        ('Personal info', {
            'fields': ('first_name', 'last_name', 'username', 'phone')
        }),

        ('Professional info', {
            'fields': (
                'pcn_number',
                'year_qualified',
                'area_of_practice',
                'years_experience',
            )
        }),

        ('Documents', {
            'fields': ('pcn_certificate', 'passport_photo')
        }),

        ('Approval & Status', {
            'fields': ('status',)
        }),

        ('Permissions', {
            'fields': (
                'is_staff',
                'is_superuser',
                'is_active',
                'groups',
                'user_permissions',
            )
        }),

        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',  # use email for adding new users
                'username',
                'first_name',
                'last_name',
                'phone',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            )
        }),
    )

    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)  # order by email
