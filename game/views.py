import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from utils import http, codes, messages

from .models import Deck, Room, Card
from utils.constants import SUITS

User = get_user_model()


def test(request):
    return HttpResponse("<h1>test</h1>")


@csrf_exempt
def show_visual(request):
    try:
        deck_id = int(request.GET.get("deck_id") or request.POST.get("deck_id"))
        deck = Deck.objects.get(id=deck_id)
    except ObjectDoesNotExist:
        deck = Deck.objects.last()
    except:
        deck = Deck.objects.last()
    # except
    index = 0
    hand01 = hand02 = hand03 = hand04 = None
    my_list = list()
    if deck:
        if deck.moves.exists():
            for move in deck.moves.all().reverse():
                if move.first_move:
                    my_list.append(Card.objects.get(id=move.card_id))
                    # my_list.append(deck.cards.get(deck__moves__card_id=move.card_id))
                    break
                my_list.append(Card.objects.get(id=move.card_id))
            current_cards = list()
            for i in reversed(my_list):
                current_cards.append(i)
        else:
            current_cards = None
        for hand in deck.hands.all():
            index += 1
            if index == 1:
                hand01 = hand
            elif index == 2:
                hand02 = hand
            elif index == 3:
                hand03 = hand
            elif index == 4:
                hand04 = hand
        context = {
            "deck": deck,
            "hand01": hand01,
            "hand02": hand02,
            "hand03": hand03,
            "hand04": hand04,
            "current_cards": current_cards,
        }
    else:
        context = {
        }
    return render(request, "game/visual.html", context)


def different_users(user01, user02, user03, user04):
    """
        Check if all the users are different
    """
    return user01 != user02 and user01 != user03 and user01 != user04 and user02 != user03 and user02 != user04 and user03 != user04


@http.json_response()
@http.requires_token()
@csrf_exempt
def create_room(request, user):
    if user.rooms.filter(active=True).count() > 0:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ACTIVE_ROOM_EXISTS)
    room = Room.objects.create(owner=user, user01=user)
    return {
        "room": room.json(),
    }


@http.json_response()
@http.requires_token()
@http.required_parameters(["room_id"])
@csrf_exempt
def enter_room(request, user):
    try:
        room = Room.objects.get(pk=int(request.POST.get("room_id")),  active=True)
    except ObjectDoesNotExist:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    is_full, free_place = room.is_full()
    if room.inside(user):
        inside = True
    else:
        inside = False
    if not inside:
        if is_full:
            return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_IS_FULL)
        else:
            if free_place == 1 and user == room.owner:
                room.user01 = user
            elif free_place == 2:
                room.user02 = user
            elif free_place == 3:
                room.user03 = user
            elif free_place == 4:
                room.user04 = user
        room.user01_ready = False
        room.user02_ready = False
        room.user03_ready = False
        room.user04_ready = False
        room.save()

    return {
        "room": room.json(),
        "entered": not inside,
    }


@http.json_response()
@http.requires_token()
@http.required_parameters(["room_id"])
@csrf_exempt
def leave_room(request, user):
    try:
        room_id = int(request.POST.get("room_id"))
        room = Room.objects.filter(
            Q(pk=room_id, user01=user, active=True) | Q(pk=room_id, user02=user, active=True) | Q(pk=room_id, user03=user, active=True) | Q(pk=room_id, user04=user, active=True)).last()
        if room is None:
            return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    except ObjectDoesNotExist:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    if room.user02 == user:
        room.user02 = None
    elif room.user03 == user:
        room.user03 = None
    elif room.user04 == user:
        room.user04 = None
    elif room.user01 == user:
        room.user01 = None
    room.user01_ready = False
    room.user02_ready = False
    room.user03_ready = False
    room.user04_ready = False
    room.save()
    return {
        "room": room.json(),
    }


@http.json_response()
@http.requires_token()
@http.required_parameters(["user_id"])
@csrf_exempt
def remove_user(request, user):
    try:
        room = user.rooms.get(active=True)
        new_user = User.objects.get(pk=int(request.POST.get("user_id") or request.GET.get("user_id")))
        if user == new_user or not room.inside(new_user):
            return http.code_response(code=codes.BAD_REQUEST, message=messages.USER_NOT_FOUND)
    except ObjectDoesNotExist:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    if room.user02 == new_user:
        room.user02 = None
    elif room.user03 == new_user:
        room.user03 = None
    elif room.user04 == new_user:
        room.user04 = None
    room.user01_ready = False
    room.user02_ready = False
    room.user03_ready = False
    room.user04_ready = False
    room.save()
    return {
        "room": room.json(),
    }


@http.json_response()
@http.requires_token()
@http.required_parameters(["room_id"])
@csrf_exempt
def ready(request, user):
    try:
        room_id = int(request.POST.get("room_id"))
        room = Room.objects.filter(
            Q(pk=room_id, user01=user, active=True) | Q(pk=room_id, user02=user, active=True) | Q(pk=room_id, user03=user, active=True) | Q(pk=room_id, user04=user, active=True)).last()
        if room is None:
            return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    except ObjectDoesNotExist:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    if user == room.user01:
        room.user01_ready = True
    elif user == room.user02:
        room.user02_ready = True
    elif user == room.user03:
        room.user03_ready = True
    elif user == room.user04:
        room.user04_ready = True
    room.save()
    if room.all_ready:
        deck, created = Deck.objects.get_or_create(room=room, active=True)
        if created:
            room.started = True
            room.save()
    return {
        "room": room.json(),
    }


@http.json_response()
@http.requires_token()
@http.required_parameters(["room_id", "trump"])
@csrf_exempt
def create_deck(request, user):
    try:
        room = Room.objects.get(pk=int(request.POST.get("room_id")), owner=user, active=True)
    except ObjectDoesNotExist:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    trump = int(request.POST.get("trump") or request.GET.get("trump"))
    if trump not in [suit[0] for suit in SUITS]:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.INVALID_PARAMS, field="trump")
    deck = Deck.objects.create(room=room, trump=trump)
    return {
        "deck": deck.json(),
    }


@http.json_response()
@http.requires_token(optional=True)
@http.required_parameters(["deck_id"])
@csrf_exempt
def show_deck(request, user):
    deck_id = int(request.POST.get("deck_id") or request.GET.get("deck_id"))
    try:
        deck = Deck.objects.get(pk=deck_id, active=True)
    except ObjectDoesNotExist:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.DECK_NOT_FOUND)
    return {
        "deck": deck.json(),
    }


@http.json_response()
@http.requires_token()
@http.required_parameters(["room_id", "deck_id", "card_id"])
@csrf_exempt
def make_move(request, user):
    try:
        room = Room.objects.get(pk=int(request.POST.get("room_id") or request.GET.get("room_id")), active=True)
        if not room.inside(user):
            return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    except ObjectDoesNotExist:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    try:
        deck = Deck.objects.get(pk=(request.POST.get("deck_id") or request.GET.get("deck_id")), room=room,
                                active=True)
        if deck.total_moves > 31:
            return http.code_response(code=codes.BAD_REQUEST, message=messages.DECK_NOT_FOUND)
    except ObjectDoesNotExist:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.DECK_NOT_FOUND)

    error_message = deck.make_move(request=request, user=user)
    if error_message:
        return error_message

    return {
        "deck": deck.json(),
    }




