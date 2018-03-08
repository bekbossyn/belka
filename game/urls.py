from django.conf.urls import url

from . import views

app_name = "game"

urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^deck/show_visual/$', views.show_visual, name='show_visual'),
    url(r'^deck/create/$', views.create_deck, name='create_deck'),
    url(r'^deck/show/$', views.show_deck, name='show_deck'),
]
