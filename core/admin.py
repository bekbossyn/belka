from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MainUserChangeForm, MainUserCreationForm
from .models import MainUser, Activation, Exchange


@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    form = MainUserChangeForm
    add_form = MainUserCreationForm

    list_display = (
        'id',
        'phone',
        'email',
        # 'fb_id',
        # 'insta_id',
        # 'vk_id',
        'name',
        'last_login',
        # 'country',
        'is_active',
        'is_admin',
        'timestamp',
        'player_ids',
    )

    list_filter = ('is_admin', 'is_active',)

    search_fields = ('phone', 'email', 'name',)

    ordering = ('-timestamp',)

    fieldsets = (
        (None, {'fields': (
                    'phone',
                    'email',
                    'name',
                    'avatar',
            )}),
        ('Password', {'fields': ('password', )}),  # we can change password in admin-site
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
        ('Info', {'fields': ('language', 'player_ids',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'name', 'password1', 'password2',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin', )}),
    )


@admin.register(Activation)
class ActivationAdmin(admin.ModelAdmin):
    # list_display = ('id', 'phone', 'email', 'fb_id', 'vk_id', 'insta_id', 'code', 'used', 'avatar')
    list_display = ('id', 'phone', 'email', 'code', 'used', 'avatar',)

    list_filter = ('used',)


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'sending', 'receiving', 'data_and_time', 'timestamp',)

    # list_filter = ('date_and_time',)

    ordering = ('-timestamp',)



