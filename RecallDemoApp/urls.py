from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('allbots/', views.allbots, name='allbots'),
    path('allbots/details/<uuid:BotID>', views.details, name='details'),
    path('createbot/', views.createbot, name='createbot'),
    path('allbots/details/novideo/', views.novideo, name='novideo'),
    path('allbots/details/<uuid:BotID>/transcription/', views.transcription, name='transcription'),
]
