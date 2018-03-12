from django.conf.urls import url

from . import views

app_name = "game"

urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^room/create/$', views.create_room, name='create_room'),
    url(r'^room/enter/$', views.enter_room, name='enter_room'),
    url(r'^room/leave/$', views.leave_room, name='leave_room'),
    url(r'^room/remove/$', views.remove_user, name='remove_user'),
    url(r'^room/deck/show_visual/$', views.show_visual, name='show_visual'),
    url(r'^room/deck/create/$', views.create_deck, name='create_deck'),
    url(r'^deck/show/$', views.show_deck, name='show_deck'),
    url(r'^start/$', views.start_game, name='start_game'),
]
