
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.friend_pk = self.scope['url_route']['kwargs']['recId']
        self.user=self.scope['user']
        self.combine = f"{self.friend_pk}_{self.user.pk}"
        self.unique_group_name= ''.join(sorted(self.combine))
        self.room_group_name= f'chat__myroom_{self.unique_group_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
      

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
    
    async def receive(self,text_data):
        print("HEELo",text_data)
        text_data_json=json.loads(text_data)
        message = text_data_json['message']
        rec_id = text_data_json['rec_id']
        self.user_id = self.scope['user'].id

        try:
            room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_group_name)
        except:
            room = await database_sync_to_async(ChatRoom.objects.create)(name=self.room_group_name)

        rec_obj = await database_sync_to_async(Users.objects.get)(pk=rec_id)
        chat = Chats(
			msg=message,
			sender_id =self.scope['user'],
            rec_id = rec_obj,
			room=room
		)
        await database_sync_to_async(chat.save)()
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'message':message,
                'user_id':self.user_id
            }
        ) 

    async def chat_message(self,event):
        message=event['message']
        user_id=event['user_id']
        user=await database_sync_to_async(Users.objects.get)(pk=user_id)
        name=user.name
        await self.send(text_data=json.dumps({
            'message':message,
            'user_id':user_id,
            'name':name
        }))

