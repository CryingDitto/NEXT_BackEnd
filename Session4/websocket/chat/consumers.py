from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("ChatConsumer connected.");
        self.accept()

    def disconnect(self, close_code):
        pass

    # html에서의 onmessage와 같은 것
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        self.send(text_data = json.dumps({
            "sender":sender,
            "message":message
        }))