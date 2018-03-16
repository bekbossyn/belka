from django.contrib import admin

from .models import GameSetting


@admin.register(GameSetting)
class ActivationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'on_save', 'on_full', 'ace_allowed', 'on_eggs', 'timestamp',)

    list_filter = ('on_save', 'on_full', 'ace_allowed', 'on_eggs',)

