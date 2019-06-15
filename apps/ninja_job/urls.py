from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ninja', views.index),
    url(r'^game_over', views.end_screen),
    url(r'^new_game', views.new_session),
    url(r'^$', views.init_session),
    url(r'^(?P<loc>[a-zA-Z]+)$', views.process),
]