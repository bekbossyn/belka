from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def test(request):
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
    context = {
        "hand_01": deck.get_active_hand(deck.hand01),
        "hand_02": deck.get_active_hand(deck.hand02),
        "hand_03": deck.get_active_hand(deck.hand03),
        "hand_04": deck.get_active_hand(deck.hand04),
    }
    return render(request, "game/visual.html", context)



