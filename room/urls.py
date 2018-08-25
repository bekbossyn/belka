from django.conf.urls import url

from . import views

app_name = "room"

urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^deck/show_visual/$', views.show_visual, name='show_visual'),
    url(r'^create/$', views.create_room, name='create_room'),
    url(r'^enter/$', views.enter_room, name='enter_room'),
    url(r'^leave/$', views.leave_room, name='leave_room'),
    url(r'^remove_user/$', views.remove_user, name='remove_user'),
    url(r'^ready/$', views.ready, name='ready'),
    url(r'^deck/create/$', views.create_deck, name='create_deck'),
    url(r'^deck/make_move/$', views.make_move, name='make_move'),
    url(r'^deck/allowed/$', views.get_allowed, name='get_allowed'),
    url(r'^deck/show/$', views.show_deck, name='show_deck'),
    # url(r'^start/$', views.start_game, name='start_game'),
    url(r'^all/$', views.all_rooms, name='all_rooms'),
]

