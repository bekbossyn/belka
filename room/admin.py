from django.contrib import admin

from .models import Deck, Hand, Card, Room, Move


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'owner', 'user01', 'user01_ready', 'user02', 'user02_ready', 'user03', 'user03_ready', 'user04',
        'user04_ready', 'all_ready', 'has_jack_of_clubs', 'trump_is_hidden', 'started', 'full', 'active', 'timestamp',)

    list_filter = ('owner', 'started', 'full', 'active',)

    readonly_fields = ('timestamp', )


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('pk', 'room', 'trump', 'next_move', 'total_moves', 'active', 'timestamp',)

    list_filter = ('room', 'total_moves', 'active',)

    readonly_fields = ('timestamp', )


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('pk', 'deck', 'user', 'card_id', 'first_move', 'active', 'timestamp',)

    list_filter = ('deck', 'user', 'first_move', 'active',)

    readonly_fields = ('timestamp',)


@admin.register(Hand)
class HandAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'deck', 'active', 'timestamp',)

    list_filter = ('user', 'deck', 'active',)

    readonly_fields = ('timestamp',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('pk', 'deck', 'hand', 'name', 'value', 'worth', 'image_url', 'trump_priority', 'active', 'timestamp',)

    list_filter = ('deck', 'hand', 'active',)

    readonly_fields = ('timestamp',)


