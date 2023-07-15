from django.urls import path,re_path
from social.consumer import ChatConsumer

websocket_urlpatterns=[
   # re_path('ws/chat/',ChatConsumer.as_asgi())
   re_path(r'^ws/chat/(?P<recId>[^/]+)/$', ChatConsumer.as_asgi()),
]