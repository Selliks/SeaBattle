from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('save_ships/', views.save_ships, name='save_ships'),
    path('play/', views.play, name='play'),
    path('shot/', views.shot, name='shot'),
    path('bot_shot/', views.bot_shot, name='bot_shot'),
]
