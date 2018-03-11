import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from utils import http, codes, messages

from .models import Deck, Room, Settings
from utils.constants import SUITS, ON_SAVE_SUM_30, ON_SAVE, ON_FULL_OPEN_FOUR, ON_FULL, ON_EGGS_OPEN_FOUR, ON_EGGS

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
        "hand_01": hand01,
        "hand_02": hand02,
        "hand_03": hand03,
        "hand_04": hand04,
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
        # if room.user01 == user:
        #     return http.code_response(code=codes.BAD_REQUEST, message=messages.INVALID_PARAMS)
    except ObjectDoesNotExist:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    is_full, free_place = room.is_full()
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
    room.save()
    return {
        "room": room.json(),
    }


@http.json_response()
@http.requires_token()
@http.required_parameters(["trump"])
@csrf_exempt
def create_deck(request, user):
    trump = int(request.POST.get("trump") or request.GET.get("trump"))
    if trump not in [suit[0] for suit in SUITS]:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.INVALID_PARAMS, field="trump")
    deck = Deck.objects.create(trump=trump)
    return {
        "deck": deck.json(),
    }


@http.json_response()
@http.required_parameters(["deck_id"])
@csrf_exempt
def show_deck(request):

    deck_id = int(request.POST.get("deck_id") or request.GET.get("deck_id"))
    deck = Deck.objects.get(pk=deck_id)
    return {
        "deck": deck.json(),
    }


# @http.json_response()
# @http.required_parameters(["deck_id"])
# @csrf_exempt
# def make_move(request):
#     try:
#         deck = Deck.objects.get(pk=(request.POST.get("deck_id") or request.GET.get("deck_id")))
#     except ObjectDoesNotExist:
#         return http.code_response(code=codes.BAD_REQUEST, message=messages.DECK_NOT_FOUND)
#     allowed_hand_list = deck.allowed_hand_list()
#     if len(allowed_hand_list) == 8:
#         # ALL moves can be made
#         move = random.randint(0, len(allowed_hand_list) - 1)
#     else:
#         #   TODO create movement
#         move = 0
#     # allowed_hand_list.remove(allowed_hand_list[move])
#     deck.deactivate(allowed_hand_list[move])
#     deck.save()
#     return {
#         "allowed": allowed_hand_list,
#         "deck": deck.json(),
#     }




