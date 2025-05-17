from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start_game, name='start_game'),
    path('play/', views.play, name='play'),
    path('shot/', views.player_shot, name='player_shot'),

]
