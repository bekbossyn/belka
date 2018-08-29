import random
from operator import itemgetter

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from belka import settings
from utils.constants import SUITS, CARD_NUMBERS, CLUBS_VALUE, SPADES_VALUE, HEARTS_VALUE, INITIAL_PLAYER_INDEX, \
    MOVES_QUEUE, TRUMP_PRIORITY_JACK, DIAMONDS_VALUE, ACE_OF_CLUBS_VALUE, ACE_OF_SPADES_VALUE, ACE_OF_HEARTS_VALUE, \
    ACE_OF_DIAMONDS_VALUE, TEAM_TOTAL_MAX_LOCAL, TEAM_TOTAL_MAX, ON_EGGS_OPEN_FOUR, ON_EGGS_OPEN_DOUBLE
from utils.image_utils import get_url
from utils.time_utils import dt_to_timestamp


class Room(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rooms', null=False, on_delete=models.CASCADE)
    user01 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='user01', on_delete=models.CASCADE)
    user01_ready = models.BooleanField(default=False)
    user02 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='user02', on_delete=models.CASCADE)
    user02_ready = models.BooleanField(default=False)
    user03 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='user03', on_delete=models.CASCADE)
    user03_ready = models.BooleanField(default=False)
    user04 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='user04', on_delete=models.CASCADE)
    user04_ready = models.BooleanField(default=False)
    has_jack_of_clubs = models.PositiveSmallIntegerField(default=0)
    trump_is_hidden = models.BooleanField(default=True)
    all_ready = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    full = models.BooleanField(default=False)
    total_team01 = models.PositiveSmallIntegerField(default=0)
    total_team02 = models.PositiveSmallIntegerField(default=0)
    previous_eggs = models.BooleanField(default=False)
    current_label = models.PositiveSmallIntegerField(default=1)
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
            "owner_id": self.owner_id,
            "user01_id": self.user01_id,
            "user01_ready": self.user01_ready,
            "user02_id": self.user02_id,
            "user02_ready": self.user02_ready,
            "user03_id": self.user03_id,
            "user03_ready": self.user03_ready,
            "user04_id": self.user04_id,
            "user04_ready": self.user04_ready,
            "all_ready": self.all_ready,
            "has_jack_of_clubs": self.has_jack_of_clubs,
            "trump_is_hidden": self.trump_is_hidden,
            "full": self.full,
            "total_team01": self.total_team01,
            "total_team02": self.total_team02,
            "active": self.active,
            "timestamp": dt_to_timestamp(self.timestamp),
            "setting": self.owner.game_setting.json(),
            "started": self.started,
            "current_label": self.current_label,
            "last_deck": self.decks.filter(active=True).last().json() if self.decks.filter(label=self.current_label).count() > 0 else None,
        }

    def list_json(self):
        return {
            "room_id": self.pk,
            "timestamp": dt_to_timestamp(self.timestamp),
            "setting": self.owner.game_setting.json(),
            "started": self.started,
        }

    class Meta:
        ordering = ['timestamp']


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
        instance.decks.filter(active=True).update(active=False)
    full, _ = instance.is_full()
    if full:
        instance.full = True
    else:
        instance.full = False
    if instance.user01 is None:
        instance.user01_ready = False
    if instance.user02 is None:
        instance.user02_ready = False
    if instance.user03 is None:
        instance.user03_ready = False
    if instance.user04 is None:
        instance.user04_ready = False
    instance.all_ready = instance.user01_ready and instance.user02_ready and instance.user03_ready and instance.user04_ready


class Deck(models.Model):
    """
        Deck is the game, the loaded cards of each game of the room.
    """
    room = models.ForeignKey(Room, related_name='decks', null=False, on_delete=models.CASCADE)
    trump = models.PositiveSmallIntegerField(choices=SUITS, default=CLUBS_VALUE)
    next_move = models.PositiveSmallIntegerField(choices=MOVES_QUEUE, default=INITIAL_PLAYER_INDEX)
    total_moves = models.PositiveSmallIntegerField(default=0)
    clubs = models.BooleanField(default=False)
    spades = models.BooleanField(default=False)
    hearts = models.BooleanField(default=False)
    diamonds = models.BooleanField(default=False)
    total_team01 = models.PositiveSmallIntegerField(default=0)
    total_team02 = models.PositiveSmallIntegerField(default=0)
    label = models.PositiveSmallIntegerField(default=1)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"deck {0} of room {1}".format(self.pk, self.room_id)

    def generate_next_move(self):
        """
            if total moves are % 4 then we decide who takes the next move
        """
        team_total_deck = 0
        if self.total_moves % 4 == 0:
            #   if it is the end of deck
            if self.total_moves == 32:
                self.next_move = self.room.decks.count() % 4 + 1
            first_card = self.cards.get(movement_index=self.total_moves - 3)
            current_card = first_card
            second_card = self.cards.get(movement_index=self.total_moves - 2)
            third_card = self.cards.get(movement_index=self.total_moves - 1)
            fourth_card = self.cards.get(movement_index=self.total_moves - 0)
            team_total_deck = first_card.worth + second_card.worth + third_card.worth + fourth_card.worth
            value_min = current_card.value // 100 * 100
            value_max = (current_card.value // 100 + 1) * 100
            if current_card.trump_priority == 0:
                #   if trumping
                if second_card.trump_priority > 0:
                    #   trump
                    current_card = second_card
                else:
                    #   both not trumps
                    if value_min < second_card.value < value_max:
                        #   масть
                        if current_card.value < second_card.value:
                            current_card = second_card
                if third_card.trump_priority > 0:
                    #   режет третий
                    if third_card.trump_priority > current_card.trump_priority:
                        current_card = third_card
                else:
                    #   третий не режет
                    if current_card.trump_priority == 0:
                        #   если текущий режет
                        #   both not trumps
                        if value_min < third_card.value < value_max:
                            #   если масть
                            if current_card.value < third_card.value:
                                current_card = third_card
                if fourth_card.trump_priority > 0:
                    #   режет третий
                    if fourth_card.trump_priority > current_card.trump_priority:
                        current_card = fourth_card
                else:
                    #   третий не режет
                    if current_card.trump_priority == 0:
                        #   если текущий режет
                        #   both not trumps
                        if value_min < fourth_card.value < value_max:
                            #   если масть
                            if current_card.value < fourth_card.value:
                                current_card = fourth_card
            else:
                #   trumping
                if second_card.trump_priority > current_card.trump_priority:
                    current_card = second_card
                if third_card.trump_priority > current_card.trump_priority:
                    current_card = third_card
                if fourth_card.trump_priority > current_card.trump_priority:
                    current_card = fourth_card
            user_id = self.moves.get(card_id=current_card.id).user.id

            #   кто ходит следующим
            #   сумма набранных очков командой
            if user_id == self.room.user01_id:
                self.total_team01 += team_total_deck
                return 1
            elif user_id == self.room.user02_id:
                self.total_team02 += team_total_deck
                return 2
            elif user_id == self.room.user03_id:
                self.total_team01 += team_total_deck
                return 3
            else:
                self.total_team02 += team_total_deck
                return 4
        else:
            return self.next_move % 4 + 1

    def allowed_list(self, trumping=False, hand=None, first_card=None):
        jack_values = [110, 210, 310, 410]
        my_list = list()
        value_min = first_card.value // 100 * 100
        value_max = (first_card.value // 100 + 1) * 100
        kwargs_exclude = dict()
        value__in = list()
        if not self.room.owner.game_setting.ace_allowed:
            if first_card.value not in range(value_min, value_max):
                if not self.clubs:
                    value__in.append(ACE_OF_CLUBS_VALUE)
                if not self.spades:
                    value__in.append(ACE_OF_SPADES_VALUE)
                if not self.hearts:
                    value__in.append(ACE_OF_HEARTS_VALUE)
                if not self.diamonds:
                    value__in.append(ACE_OF_DIAMONDS_VALUE)
        if len(value__in) > 0:
            kwargs_exclude["value__in"] = value__in
        if trumping:
            cards = hand.cards.filter(active=True, trump_priority__gt=0)
            #   no trumps
            if cards.count() == 0:
                cards = hand.cards.filter(active=True).exclude(**kwargs_exclude)
        else:
            cards = hand.cards.filter(active=True, value__gt=value_min, value__lt=value_max).exclude(
                value__in=jack_values).exclude(**kwargs_exclude)
            #   no cards with such values(нету такой масти)
            if cards.count() == 0:
                cards = hand.cards.filter(active=True).exclude(**kwargs_exclude)
        for card in cards:
            my_list.append(card)
        return my_list

    def make_move(self, request, user):
        """
            return error_message or
            returns None, and makes move
        """
        from utils import codes, messages, http
        #   if not queue of the user to make move
        if (self.next_move == 1 and user != self.room.user01) or (self.next_move == 2 and user != self.room.user02) or (
                self.next_move == 3 and user != self.room.user03) or (self.next_move == 4 and user != self.room.user04):
            return http.code_response(code=codes.BAD_REQUEST, message=messages.ACTION_NOT_ALLOWED)

        try:
            card_id = int(request.POST.get("card_id") or request.GET.get("card_id"))
        except ObjectDoesNotExist:
            return http.code_response(code=codes.BAD_REQUEST, message=messages.INVALID_PARAMS, field="card_id")
        hand = None
        index = 1
        for hand in self.hands.all():
            if index == self.next_move:
                break
            index += 1
            if index > 4:
                return http.code_response(code=codes.SERVER_ERROR, message=messages.INVALID_PARAMS,
                                          field="index of hands is out of range")
        if card_id not in [card.id for card in hand.cards.all()]:
            return http.code_response(code=codes.BAD_REQUEST, message=messages.CARD_NOT_FOUND)

        if hand.cards.get(id=card_id).active is False:
            #   if card is not active ALREADY.
            return http.code_response(code=codes.BAD_REQUEST, message=messages.ACTION_NOT_ALLOWED)
        if self.total_moves >= 32:
            return http.code_response(code=codes.SERVER_ERROR, message=messages.INVALID_PARAMS,
                                      field="total_moves of deck is out of range")
        #   MAIN process
        if self.total_moves % 4 == 0:
            #   if move is FIRST MOVE of CURRENT Move consisting of 32 turns
            #   deactivate previous move histories of deck
            self.moves.update(active=False)
            Move.objects.create(deck=self, user=user, card_id=card_id, first_move=True)
            hand.cards.filter(pk=card_id).update(active=False, movement_index=self.total_moves + 1)
            self.total_moves = self.total_moves + 1
            self.next_move = self.next_move % 4 + 1
            self.save()
        else:
            my_card = Card.objects.get(pk=card_id)
            first_move = self.moves.filter(first_move=True).last()
            first_card = Card.objects.get(id=first_move.card_id)
            allowed_list = self.allowed_list(trumping=first_card.trump_priority > 0, hand=hand, first_card=first_card)
            if my_card not in allowed_list:
                return http.code_response(code=codes.BAD_REQUEST, message=messages.ACTION_NOT_ALLOWED)
            # if len(allowed_list) == 1:
            self.moves.update(active=False)
            Move.objects.create(deck=self, user=user, card_id=card_id, first_move=False)
            hand.cards.filter(pk=card_id).update(active=False, movement_index=self.total_moves + 1)
            #   next moves the player who takes 4 cards of current moves
            self.total_moves = self.total_moves + 1
            self.next_move = self.generate_next_move()
            self.save()

    def json(self, active=True):
        return {
            "deck_id": self.pk,
            "trump": self.trump,
            "hands": [hand.json(active=active) for hand in self.hands.filter(active=active)],
            "next_move": self.next_move,
            "total_moves": self.total_moves,
            "total_team01": self.total_team01,
            "total_team02": self.total_team02,
            "label": self.label,
            "active": self.active,
            "timestamp": dt_to_timestamp(self.timestamp),
        }

    class Meta:
        ordering = ['timestamp']


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
    """
        creates the deck with random hands and cards.
        deactivates all the decks of the room except last created
        also creates the trump according to the room's has_jack_of_clubs value
    """
    #   TODO if total moves == 32:
    #   TODO count, hands, count room, finished or not, create next deck, if not finished.
    last = instance.room.decks.last()
    #   NOT the beginning.
    if instance.room.has_jack_of_clubs != 0:
        #   define new trump.
        trump = -1
    else:
        trump = 1

    #TODO Fix Count by Counting with LABEL of room and deck SAME
    instance.room.trump_is_hidden = instance.room.decks.filter(label=instance.room.current_label).count() <= 1
    instance.room.save()

    if instance.hands.count() == 0:
        bag = list()
        for suit in SUITS:
            for card_number in CARD_NUMBERS:
                # bag.append(card_to_number(instance.trump, suit, card_number))
                bag.append(card_to_number(trump, suit, card_number))   #   at the beginning the trump is unknown
        randomized_bag = list()
        while len(bag):
            #   a <= n <= b
            #   random.randint(a,b)
            random_number = random.randint(0, len(bag) - 1)
            randomized_bag.append(bag[random_number])
            bag.remove(bag[random_number])
        #   search the jack_of_clubs    for defining trump
        if trump == -1:
            for i in range(4):
                hand = randomized_bag[(i * 8):((i * 8) + 8)]
                for card in hand:
                    if card["trump_priority"] == TRUMP_PRIORITY_JACK * 40:
                        if (i + 1) == instance.room.has_jack_of_clubs:
                            trump = 1
                        elif (i + 1) % 2 == instance.room.has_jack_of_clubs % 2:
                            trump = 2
                        elif (instance.room.has_jack_of_clubs % 4 + 1) == (i + 1):
                            trump = 3
                        else:
                            trump = 4
                        break
            #   setting current trump
            instance.room.decks.filter(pk=last.pk).update(trump=trump, label=instance.room.current_label)
            for card in randomized_bag:
                if card["value"] // 100 == trump:
                    for card_number in CARD_NUMBERS:
                        if card["value"] % 100 == card_number[0]:
                            if card["name"] not in ["jack_of_clubs", "jack_of_spades", "jack_of_hearts", "jack_of_diamonds"]:
                                card["trump_priority"] = card_number[2]
                                break

        for i in range(4):
            if i == 0:
                user = instance.room.user01
            elif i == 1:
                user = instance.room.user02
            elif i == 2:
                user = instance.room.user03
            else:
                user = instance.room.user04
            hand = Hand.objects.create(deck=instance, user=user)
            sorted_bag = sort_by_trump(trump, randomized_bag[(i * 8):((i * 8) + 8)])
            for j in range(len(sorted_bag)):
                # current_card = randomized_bag[i * 8 + j]
                current_card = sorted_bag[j]
                name = current_card["name"]
                value = current_card["value"]
                worth = current_card["worth"]
                image_url = current_card["image_url"]
                trump_priority = current_card["trump_priority"]
                Card.objects.create(deck=instance, hand=hand, name=name, value=value, worth=worth, image_url=image_url,
                                    trump_priority=trump_priority)
                #   has the FIRST
                if trump_priority == TRUMP_PRIORITY_JACK * 40 and instance.room.trump_is_hidden:
                    instance.room.has_jack_of_clubs = i + 1
    #   if not the first game, trump is not hidden.
    #TODO correction, which needs to be checked carefully

    #   setting ace allowed
    if instance.trump == CLUBS_VALUE:
        instance.clubs = True
    elif instance.trump == SPADES_VALUE:
        instance.spades = True
    elif instance.trump == HEARTS_VALUE:
        instance.hearts = True
    elif instance.trump == DIAMONDS_VALUE:
        instance.diamonds = True
    if instance.room.owner.game_setting.ace_allowed:
        instance.clubs = True
        instance.spades = True
        instance.hearts = True
        instance.diamonds = True
    #   in order to avoid infinite recursion in post saving method.
    instance.room.decks.filter(pk=last.pk).update(clubs=instance.clubs,
                                                  spades=instance.spades,
                                                  hearts=instance.hearts,
                                                  diamonds=instance.diamonds)

    instance.room.decks.filter(active=True, label=instance.room.current_label).exclude(pk=last.pk).update(active=False)
    #   Если козырь в начале был
    team01 = [1, 3]
    team02 = [2, 4]
    if instance.trump > 2:      #    Trump is Hearts or Diamonds
        if instance.room.has_jack_of_clubs % 2 == 0:    #   Trump user of room is 2 or 4
            current_trump_team = 1
        else:
            current_trump_team = 2
    else:                       #    Trump is Clubs or Spades
        if instance.room.has_jack_of_clubs % 2 == 0:    #   Trump user of room is 2 or 4
            current_trump_team = 2
        else:
            current_trump_team = 1

    if instance.total_moves >= 32 and instance.total_team01 + instance.total_team02 == TEAM_TOTAL_MAX_LOCAL:
        #TODO 120 очков НЕ ОЗНАЧАЕТ ГОЛАЯ. Требуется дополнительная проверка
        if instance.total_team01 == TEAM_TOTAL_MAX_LOCAL:
            #   голая реализована командой 01
            if instance.room.owner.game_setting.on_full == ON_EGGS_OPEN_FOUR:
                #   откывается 4 глаза команда 01
                instance.room.total_team01 += 4
                instance.room.save()
            else:
                #   голая = партия Выигрывает команда 01
                instance.room.total_team01 = TEAM_TOTAL_MAX
                instance.room.save()
            pass
        elif instance.total_team02 == TEAM_TOTAL_MAX_LOCAL:
            #   голая реализована командой 02
            if instance.room.owner.game_setting.on_full == ON_EGGS_OPEN_FOUR:
                #   откывается 4 глаза команда 02
                instance.room.total_team02 += 4
                instance.room.save()
            else:
                #   голая = партия Выигрывает команда 02
                instance.room.total_team02 = TEAM_TOTAL_MAX
                instance.room.save()

            pass
        elif instance.room.previous_eggs:
            #   предыдущая игра ЯЙЦА
            if instance.room.owner.game_setting.on_eggs == ON_EGGS_OPEN_FOUR:
                #   открывается 4 глаза
                if instance.total_team01 > instance.total_team02:
                    #   открывает команда 01
                    instance.room.total_team01 += 4
                    instance.room.previous_eggs = False
                    instance.room.save()
                elif instance.total_team01 < instance.total_team02:
                    #   открывает команда 02
                    instance.room.total_team02 += 4
                    instance.room.previous_eggs = False
                    instance.room.save()
                else:
                    #TODO опять ЯЙЦА
                    pass
            elif instance.room.owner.game_setting.on_eggs == ON_EGGS_OPEN_DOUBLE:
                #   открывается удвоенно
                if instance.total_team01 > instance.total_team02:
                    #   открывает команда 01
                    if current_trump_team in team01:
                        # козырь с команды 01
                        if instance.total_team02 < instance.room.owner.game_setting.on_save:
                            #   команда 02 не набрала СПАС
                            instance.room.total_team01 += 4
                        else:
                            #   команда 02 набрала СПАС
                            instance.room.total_team01 += 2
                        instance.room.previous_eggs = False
                        instance.room.save()
                    elif current_trump_team in team02:
                        # козырь с команды 02
                        if instance.total_team02 < instance.room.owner.game_setting.on_save:
                            #   команда 02 не набрала СПАС
                            instance.room.total_team01 += 6
                        else:
                            #   команда 02 набрала СПАС
                            instance.room.total_team01 += 4
                        instance.room.previous_eggs = False
                        instance.room.save()
                elif instance.total_team01 < instance.total_team02:
                    #   открывает команда 02
                    if current_trump_team in team01:
                        # козырь с команды 01
                        if instance.total_team01 < instance.room.owner.game_setting.on_save:
                            #   команда 01 не набрала СПАС
                            instance.room.total_team02 += 6
                        else:
                            #   команда 01 набрала СПАС
                            instance.room.total_team02 += 4
                        instance.room.previous_eggs = False
                        instance.room.save()
                    elif current_trump_team in team02:
                        # козырь с команды 02
                        if instance.total_team01 < instance.room.owner.game_setting.on_save:
                            #   команда 01 не набрала СПАС
                            instance.room.total_team02 += 4
                        else:
                            #   команда 01 набрала СПАС
                            instance.room.total_team02 += 2
                        instance.room.previous_eggs = False
                        instance.room.save()
                else:
                    #TODO опять ЯЙЦА
                    pass

        elif instance.total_team01 < instance.room.owner.game_setting.on_save:
            if current_trump_team in team01:
                #   если команда 01 не набрала спас и козырь с команды 01
                instance.room.total_team02 += 3
                instance.room.save()
            else:
                #   если команда 01 не набрала спас и козырь с команды 02
                instance.room.total_team02 += 2
                instance.room.save()
        elif instance.total_team02 < instance.room.owner.game_setting.on_save:
            if current_trump_team in team02:
                #   если команда 02 не набрала спас и козырь с команды 02
                instance.room.total_team01 += 3
                instance.room.save()
            else:
                #   если команда 02 не набрала спас и козырь с команды 01
                instance.room.total_team01 += 2
                instance.room.save()
        else:
            if instance.total_team01 > instance.total_team02:
                if current_trump_team in team01:
                    instance.room.total_team01 += 1
                    instance.room.save()
                else:
                    instance.room.total_team01 += 2
                    instance.room.save()
            elif instance.total_team01 < instance.total_team02:
                if current_trump_team in team02:
                    instance.room.total_team02 += 1
                    instance.room.save()
                else:
                    instance.room.total_team02 += 2
                    instance.room.save()
            else:
                #   TODO ЯЙЦА
                instance.room.previous_eggs = True
                instance.room.save()
                #   TODO create deck to play eggs
                pass
        if instance.room.total_team01 >= TEAM_TOTAL_MAX or instance.room.total_team02 >= TEAM_TOTAL_MAX:
            #   TODO Закончить игру
            #   Обнуление и Ожидание игроков
            instance.room.user01_ready = False
            instance.room.user02_ready = False
            instance.room.user03_ready = False
            instance.room.user04_ready = False
            instance.room.started = False
            instance.room.total_team01 = 0
            instance.room.total_team02 = 0
            instance.room.trump_is_hidden = True
            instance.room.has_jack_of_clubs = 0
            instance.room.current_label = instance.room.current_label + 1
            instance.room.save()
            #    деактивирование Всех Активных колод Комнаты
            instance.room.decks.last().hands.filter(active=True).update(active=False)
            instance.room.decks.all().update(active=False)
            pass
        else:
            instance.room.decks.last().hands.filter(active=True).update(active=False)
            instance.room.decks.filter(active=True).update(active=False)
            #   create new deck
            if instance.total_moves == 32:
                next_move = instance.room.decks.filter(label=instance.room.current_label).count() % 4 + 1
                #   actually, it will CREATE
                deck, created = Deck.objects.get_or_create(room=instance.room, active=True, next_move=next_move, label=instance.room.current_label)
                # instance.room.current_label = instance.room.current_label + 1
                # instance.room.save()
            else:
                next_move = instance.next_move
                #   actually, it will GET
                deck, created = Deck.objects.get_or_create(room=instance.room, active=True, next_move=next_move, label=instance.room.current_label)


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


class Move(models.Model):
    """
        History of moves of each 4 turns of the Deck
    """
    deck = models.ForeignKey(Deck, null=False, related_name='moves', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='moves', on_delete=models.CASCADE)
    card_id = models.IntegerField(default=0)
    first_move = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"MoveHistory {0} of deck {1}".format(self.pk, self.deck_id)

    def json(self, active=True):
        return {
            "move_id": self.pk,
            "user_id": self.user_id,
            "card_id": self.card_id,
            "first_move": self.first_move,
            "active": self.active,
            "timestamp": dt_to_timestamp(self.timestamp),
        }

    class Meta:
        ordering = ['timestamp']


class Hand(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='hands', on_delete=models.CASCADE)
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
        ordering = ['timestamp']


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
    deck = models.ForeignKey(Deck, related_name='cards', null=False, on_delete=models.CASCADE)
    hand = models.ForeignKey(Hand, related_name='cards', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    value = models.PositiveSmallIntegerField(default=0)
    worth = models.PositiveSmallIntegerField(default=0)
    image_url = models.CharField(max_length=100, default="")
    trump_priority = models.PositiveSmallIntegerField(default=0)
    movement_index = models.PositiveSmallIntegerField(default=0)

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
        ordering = ['timestamp']


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







