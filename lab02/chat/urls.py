from django.urls import path
from .views import *

urlpatterns = [
    path('chat/', chat_main, name='rooms'),  # Main chat lobby
    path('room/<str:room_name>/', room, name='room'),  # Room-specific URL
]


