from django.conf.urls import url

from . import views

app_name = "game"

urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^deck/show/$', views.show, name='show'),
    url(r'^deck/create/$', views.create_deck, name='create_deck'),
]
