from django.urls import path
from .consumers import OwnersNotificationsConsumer

websocket_urlpatterns = [
    path('ws/message/') # Замінити
]