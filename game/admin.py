from django.contrib import admin

from .models import Deck, Hand, Card, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'owner', 'user01', 'user01_ready', 'user02', 'user02_ready', 'user03', 'user03_ready', 'user04',
        'user04_ready', 'all_ready', 'started', 'full', 'active', 'timestamp',)

    readonly_fields = ('timestamp', )


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('pk', 'trump', 'next_move', 'total_moves', 'active', 'timestamp',)

    readonly_fields = ('timestamp', )


@admin.register(Hand)
class HandAdmin(admin.ModelAdmin):
    list_display = ('pk', 'deck', 'active', 'timestamp',)

    readonly_fields = ('timestamp',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('pk', 'hand', 'name', 'value', 'worth', 'image_url', 'trump_priority', 'active', 'timestamp',)

    readonly_fields = ('timestamp',)


