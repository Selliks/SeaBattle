from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),            # сторінка розстановки кораблів
    path('save_ships/', views.save_ships, name='save_ships'),  # збереження розстановки
    path('play/', views.play, name='play'),         # ігровий екран
    path('shot/', views.shot, name='shot'),         # постріл гравця
    path('bot_shot/', views.bot_shot, name='bot_shot'),  # постріл бота
]
