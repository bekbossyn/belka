from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from game.models import Deck


def test(request):
    Deck.objects.create(trump=4)
    return HttpResponse("<h1>test</h1>")


@csrf_exempt
def test_visual(request):
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



