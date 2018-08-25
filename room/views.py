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


@http.json_response()
def test(request):
    """
        @apiDescription Тест
        <br>Тестирование простого метода `GET`
        @api {get} /room/test/ 01. Тест [test]
        @apiGroup 03. Room
        @apiSuccess {json} result Json
    """
    return {}
    # return HttpResponse("<h1>test</h1>")


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
            "team01_local_total": deck.total_team01,
            "team02_local_total": deck.total_team02,
            "team01_total": deck.room.total_team01,
            "team02_total": deck.room.total_team02,
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
    """
        @apiDescription Создание комнаты
        <br>Создание комнаты. Метод `post`
        @api {post} /room/create/ 02. Создание комнаты [create_room]
        @apiGroup 03. Room
        @apiHeader {String} auth-token Токен авторизации
        @apiSuccess {json} result Json
    """
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
    """
        @apiDescription Вход в комнату
        @api {post} /room/enter/ 03. Вход в комнату [enter_room]
        @apiGroup 03. Room
        @apiHeader {String} auth-token Токен авторизации
        @apiParam {integer} room_id Room id
        @apiSuccess {json} result Json
    """
    try:
        room = Room.objects.get(pk=int(request.POST.get("room_id") or request.GET.get("room_id")),  active=True)
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
    """
        @apiDescription Покинуть комнату
        <br>Вход в комнату с id room_id
        @api {post} /room/leave/ 04. Покинуть комнату [leave_room]
        @apiGroup 03. Room
        @apiHeader {String} auth-token Токен авторизации
        @apiParam {integer} room_id Room id
        @apiSuccess {json} result Json
    """
    try:
        room_id = int(request.POST.get("room_id") or request.GET.get("room_id"))
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
    """
        @apiDescription Удалить игрока
        <br>Удалить игрока из комнаты с id `user_id`
        @api {post} /room/remove_user/ 05. Удалить игрока [remove_user]
        @apiGroup 03. Room
        @apiHeader {String} auth-token Токен авторизации
        @apiParam {integer} user_id User id
        @apiSuccess {json} result Json
    """
    try:
        room = user.rooms.get(active=True)
        new_user = User.objects.get(pk=int(request.POST.get("user_id") or request.GET.get("user_id")))
        if user == new_user or not room.inside(new_user):
            return http.code_response(code=codes.BAD_REQUEST, message=messages.USER_NOT_FOUND)
    except ObjectDoesNotExist:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ROOM_NOT_FOUND)
    if room.started:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ACTION_NOT_ALLOWED)
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
    """
        @apiDescription Готов
        <br>Нажатие кнопки ГОТОВ
        @api {post} /room/ready/ 06. Готов [ready]
        @apiGroup 03. Room
        @apiHeader {String} auth-token Токен авторизации
        @apiParam {integer} room_id Room id
        @apiSuccess {json} result Json
    """
    try:
        room_id = int(request.POST.get("room_id") or request.GET.get("room_id"))
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
    """
        @apiDescription Создать колоду
        <br>Создать колоду в комнате с id `room_id` и козырем `trump`
        @api {post} /room/deck/create/ 07. Создать комнату [create_deck]
        @apiGroup 03. Room
        @apiHeader {String} auth-token Токен авторизации
        @apiParam {integer} room_id Room id
        @apiParam {integer} trump Trump
        @apiSuccess {json} result Json
    """
    try:
        room = Room.objects.get(pk=int(request.POST.get("room_id") or request.GET.get("room_id")), owner=user, active=True)
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
    """
        @apiDescription Показать колоду
        <br>Показать колоду с id `deck_id`. Можно просматривать БЕЗ авторизации
        @api {post} /room/deck/show/ 08. Показать колоду [show_deck]
        @apiGroup 03. Room
        @apiHeader {String} [auth-token] Токен авторизации
        @apiParam {integer} deck_id Deck id
        @apiSuccess {json} result Json
    """
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
@http.required_parameters(["room_id", "deck_id"])
@csrf_exempt
def get_allowed(request, user):
    """
        @apiDescription Показать список разрешенных карт для хода
        <br>Показать список разрешенных карт в комнате с id `room_id` в колоде с id `deck_id`
        @api {post} /room/deck/allowed/ 09. Показать список разрешенных карт [get_allowed]
        @apiGroup 03. Room
        @apiHeader {String} auth-token Токен авторизации
        @apiParam {integer} room_id Room id
        @apiParam {integer} deck_id Deck id
        @apiSuccess {json} result Json
    """
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

    hand = None
    index = 1
    for hand in deck.hands.all():
        if index == deck.next_move:
            break
        index += 1
        if index > 4:
            return http.code_response(code=codes.SERVER_ERROR, message=messages.INVALID_PARAMS,
                                      field="index of hands is out of range")
    if hand.user != user:
        return http.code_response(code=codes.BAD_REQUEST, message=messages.ACTION_NOT_ALLOWED)

    if deck.total_moves % 4 == 0:
        #   first move
        allowed_cards = [card.json() for card in hand.cards.filter(active=True)]
    else:
        #   not first movement
        first_move = deck.moves.filter(first_move=True).last()
        first_card = Card.objects.get(id=first_move.card_id)
        allowed_cards = [card.json() for card in
                         deck.allowed_list(trumping=first_card.trump_priority > 0, hand=hand, first_card=first_card)]

    return {
        "allowed_cards": allowed_cards,
    }


@http.json_response()
@http.requires_token()
@http.required_parameters(["room_id", "deck_id", "card_id"])
@csrf_exempt
def make_move(request, user):
    """
        @apiDescription Сделать ХОД
        <br>Сделать ход картой с id `card_id` из списка разрешенных карт в комнате с id `room_id` в колоде с id `deck_id`
        @api {post} /room/deck/make_move/ 10. Сделать ХОД [make_move]
        @apiGroup 03. Room
        @apiHeader {String} auth-token Токен авторизации
        @apiParam {integer} room_id Room id
        @apiParam {integer} deck_id Deck id
        @apiParam {integer} card_id Card id
        @apiSuccess {json} result Json
    """
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
        "deck": room.decks.last().json(),
    }


@http.json_response()
@http.requires_token()
# @http.required_parameters(["room_id", "deck_id"])
@csrf_exempt
def all_rooms(request, user):
    """
        @apiDescription Список всех активных комнат
        <br>Список всех активных комнат
        @api {get} /room/all/ 11. Список всех активных комнат [all_rooms]
        @apiGroup 03. Room
        @apiHeader {String} auth-token Токен авторизации
        @apiSuccess {json} result Json
    """
    rooms = Room.objects.filter(active=True, started=False)

    return {
        "rooms_list": [room.list_json() for room in rooms],
    }

