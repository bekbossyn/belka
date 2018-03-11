import random
from operator import itemgetter

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from belka import settings
from utils.constants import SUITS, CARD_NUMBERS, CLUBS_VALUE, SPADES_VALUE, HEARTS_VALUE, INITIAL_PLAYER_INDEX, \
    MOVES_QUEUE, ON_SAVE_SUM_30, ON_FULL_OPEN_FOUR, ON_EGGS_OPEN_FOUR, ON_EGGS, ON_FULL, ON_SAVE
from utils.image_utils import get_url
from utils.time_utils import dt_to_timestamp


class Room(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rooms', null=False, on_delete=models.CASCADE)
    user01 = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, related_name='user01', on_delete=models.CASCADE)
    user02 = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, related_name='user02', on_delete=models.CASCADE)
    user03 = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, related_name='user03', on_delete=models.CASCADE)
    user04 = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, related_name='user04', on_delete=models.CASCADE)
    full = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"room {0} of user {1}".format(self.pk, self.owner_id)

    def is_full(self):
        """
            return True, -1, if room is Full
            return False, place_id if place id is Free
        """
        free_place = -1
        if not self.user01:
            free_place = 1
        elif not self.user02:
            free_place = 2
        elif not self.user03:
            free_place = 3
        elif not self.user04:
            free_place = 4
        full = self.user01 is not None and self.user02 is not None and self.user03 is not None and self.user04 is not None
        return full, free_place

    def inside(self, user=None):
        """
            return True if user is already in the room, False otherwise
        """
        return user == self.user01 or user == self.user02 or user == self.user03 or user == self.user04

    def create_deck(self, trump=SUITS[0]):
        # Deck.objects.create(trump=trump)
        self.decks.filter(active=True).update(active=False)
        self.decks.create(trump=trump)
        return self.decks.last()
        pass

    def json(self):
        return {
            "room_id": self.pk,
            "room_owner_id": self.owner_id,
            "room_user01_id": self.user01_id,
            "room_user02_id": self.user02_id,
            "room_user03_id": self.user03_id,
            "room_user04_id": self.user04_id,
            "full": self.full,
            "active": self.active,
            "timestamp": dt_to_timestamp(self.timestamp),
            "setting": self.owner.game_setting.json(),
        }

    class Meta:
        ordering = ['-timestamp']


@receiver(pre_save, sender=Room)
def room_update(sender, instance, **kwargs):
    """
        Controls updating of active, full states and closing the room
    """
    if instance.user01 is None:
        instance.active = False
        instance.user02 = None
        instance.user03 = None
        instance.user04 = None
    full, _ = instance.is_full()
    if full:
        instance.full = True
    else:
        instance.full = False


class GameSetting(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='game_setting', null=True, on_delete=models.CASCADE)
    on_save = models.IntegerField(choices=ON_SAVE, default=ON_SAVE_SUM_30)
    on_full = models.IntegerField(choices=ON_FULL, default=ON_FULL_OPEN_FOUR)
    ace_allowed = models.BooleanField(default=True)
    on_eggs = models.IntegerField(choices=ON_EGGS, default=ON_EGGS_OPEN_FOUR)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"Game setting {0} of user {1}".format(self.pk, self.owner_id)

    def json(self):
        return {
            "setting_id": self.pk,
            "user_id": self.owner_id,
            "save": self.on_save,
            "save_display": self.get_on_save_display(),
            "on_full": self.on_full,
            "on_full_display": self.get_on_full_display(),
            "ace_allowed": self.ace_allowed,
            "on_eggs": self.on_eggs,
            "on_eggs_display": self.get_on_eggs_display(),
            "timestamp": dt_to_timestamp(self.timestamp),
        }

    class Meta:
        ordering = ['-timestamp']


class Deck(models.Model):
    room = models.ForeignKey(Room, related_name='decks', null=False, on_delete=models.CASCADE)
    trump = models.PositiveSmallIntegerField(choices=SUITS, default=SUITS[0])
    next_move = models.PositiveSmallIntegerField(choices=MOVES_QUEUE, default=INITIAL_PLAYER_INDEX)
    total_moves = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"deck {0} of room {1}".format(self.pk, self.room_id)

    def json(self, active=True):
        return {
            "deck_id": self.pk,
            "trump": self.trump,
            "hands": [hand.json(active=active) for hand in self.hands.filter(active=active)],
            "next_move": self.next_move,
            "total_moves": self.total_moves,
            "active": self.active,
            "timestamp": dt_to_timestamp(self.timestamp),
        }

    class Meta:
        ordering = ['-timestamp']


@receiver(pre_save, sender=Deck)
def deck_initials(sender, instance, **kwargs):
    #   Set initials
    if instance.pk is None:
        try:
            new_pk = Deck.objects.latest('id').pk + 1
        except ObjectDoesNotExist:
            new_pk = 1

        #   Set Primary Key
        instance.pk = new_pk


def sort_by_trump(trump, my_list):
    trump_priority_list = list()
    value_priority_list = list()
    for i in range(len(my_list)):
        if my_list[i]["trump_priority"] != 0:
            trump_priority_list.append(my_list[i])
        else:
            value_priority_list.append(my_list[i])
    new_hand = list()
    trump_priority_list.sort(key=itemgetter("trump_priority"), reverse=True)
    value_priority_list.sort(key=itemgetter("value"), reverse=True)

    for i in range(len(trump_priority_list)):
        new_hand.append(trump_priority_list[i])

    clubs = 0
    spades = 0
    hearts = 0
    diamonds = 0
    #   Count of suits in the generated Deck
    for i in range(len(value_priority_list)):
        if value_priority_list[i]["value"] < 200:
            clubs += 1
        elif value_priority_list[i]["value"] < 300:
            spades += 1
        elif value_priority_list[i]["value"] < 400:
            hearts += 1
        else:
            diamonds += 1
    if trump in [CLUBS_VALUE, SPADES_VALUE]:
        if trump == CLUBS_VALUE:
            trump_min = 200
            trump_max = 300
        else:
            trump_min = 100
            trump_max = 200
        if diamonds == 0:
            #   include hearts
            for i in range(len(value_priority_list)):
                if 400 > value_priority_list[i]["value"] > 300:
                    new_hand.append(value_priority_list[i])
            #   include spades or clubs
            for i in range(len(value_priority_list)):
                if trump_max > value_priority_list[i]["value"] > trump_min:
                    new_hand.append(value_priority_list[i])
        else:
            #   include diamonds
            for i in range(len(value_priority_list)):
                if 400 < value_priority_list[i]["value"]:
                    new_hand.append(value_priority_list[i])
            #   include spades or clubs
            for i in range(len(value_priority_list)):
                if trump_max > value_priority_list[i]["value"] > trump_min:
                    new_hand.append(value_priority_list[i])
            #   include hearts [if exist]
            for i in range(len(value_priority_list)):
                if 400 > value_priority_list[i]["value"] > 300:
                    new_hand.append(value_priority_list[i])
    else:
        if trump == HEARTS_VALUE:
            trump_min = 400
            trump_max = 500
        else:
            trump_min = 300
            trump_max = 400
        if clubs == 0:
            #   include spades
            for i in range(len(value_priority_list)):
                if 300 > value_priority_list[i]["value"] > 200:
                    new_hand.append(value_priority_list[i])
            #   include hearts or diamonds
            for i in range(len(value_priority_list)):
                if trump_max > value_priority_list[i]["value"] > trump_min:
                    new_hand.append(value_priority_list[i])
        else:
            #   include clubs
            for i in range(len(value_priority_list)):
                if 200 > value_priority_list[i]["value"]:
                    new_hand.append(value_priority_list[i])
            #   include hearts or diamonds
            for i in range(len(value_priority_list)):
                if trump_max > value_priority_list[i]["value"] > trump_min:
                    new_hand.append(value_priority_list[i])
            #   include spades [if exist]
            for i in range(len(value_priority_list)):
                if 300 > value_priority_list[i]["value"] > 200:
                    new_hand.append(value_priority_list[i])
    return new_hand


@receiver(post_save, sender=Deck)
def deck_finals(sender, instance, **kwargs):
    bag = list()
    for suit in SUITS:
        for card_number in CARD_NUMBERS:
            bag.append(card_to_number(instance.trump, suit, card_number))
    randomized_bag = list()
    while len(bag):
        #   a <= n <= b
        #   random.randint(a,b)
        random_number = random.randint(0, len(bag) - 1)
        randomized_bag.append(bag[random_number])
        bag.remove(bag[random_number])

    for i in range(4):
        hand = Hand.objects.create(deck=instance)
        sorted_bag = sort_by_trump(instance.trump, randomized_bag[(i * 8):((i * 8) + 8)])
        for j in range(8):
            # current_card = randomized_bag[i * 8 + j]
            current_card = sorted_bag[j]
            name = current_card["name"]
            value = current_card["value"]
            worth = current_card["worth"]
            image_url = current_card["image_url"]
            trump_priority = current_card["trump_priority"]
            Card.objects.create(hand=hand, name=name, value=value, worth=worth, image_url=image_url,
                                trump_priority=trump_priority)
    pass


def card_to_number(trump, suit, card_number):
    card = dict()
    card["value"] = suit[0] * 100 + card_number[0]
    card["worth"] = card_number[1]
    if suit[0] == trump:
        card["trump_priority"] = card_number[2]
    else:
        card["trump_priority"] = 0
    card["name"] = card_number[3].lower() + "_of_" + suit[1].lower()
    card["image_url"] = "/static/cards/" + card["name"] + ".png"

    #   Priority for JACKS
    if card["name"] == "jack_of_clubs":
        card["trump_priority"] = 4 * 1000
    elif card["name"] == "jack_of_spades":
        card["trump_priority"] = 3 * 1000
    elif card["name"] == "jack_of_hearts":
        card["trump_priority"] = 2 * 1000
    elif card["name"] == "jack_of_diamonds":
        card["trump_priority"] = 1 * 1000
    card["active"] = True
    return card


class Hand(models.Model):
    deck = models.ForeignKey(Deck, related_name='hands', null=False, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"hand {0} of deck {1}".format(self.pk, self.deck_id)

    def json(self, active=True):
        return {
            "hand_id": self.pk,
            "cards": [card.json() for card in self.cards.filter(active=active)],
            "active": self.active,
            "timestamp": dt_to_timestamp(self.timestamp),
        }

    class Meta:
        ordering = ['-timestamp']


@receiver(pre_save, sender=Hand)
def hand_initials(sender, instance, **kwargs):
    #   Set initials
    if instance.pk is None:
        try:
            new_pk = Hand.objects.latest('id').pk + 1
        except ObjectDoesNotExist:
            new_pk = 1

        #   Set Primary Key
        instance.pk = new_pk


class Card(models.Model):
    hand = models.ForeignKey(Hand, related_name='cards', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    value = models.PositiveSmallIntegerField(default=0)
    worth = models.PositiveSmallIntegerField(default=0)
    image_url = models.CharField(max_length=100, default="")
    trump_priority = models.PositiveSmallIntegerField(default=0)

    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"card {0}, {1} hand {2}".format(self.pk, self.name, self.hand_id)

    def json(self):
        return {
            "card_id": self.pk,
            "name": self.name,
            "value": self.value,
            "worth": self.worth,
            "image_url": get_url(path=self.image_url),
            "trump_priority": self.trump_priority,
            "active": self.active,
            "timestamp": dt_to_timestamp(self.timestamp),
        }

    class Meta:
        ordering = ['-timestamp']


@receiver(pre_save, sender=Card)
def card_initials(sender, instance, **kwargs):
    #   Set initials
    if instance.pk is None:
        try:
            new_pk = Card.objects.latest('id').pk + 1
        except ObjectDoesNotExist:
            new_pk = 1

        #   Set Primary Key
        instance.pk = new_pk







