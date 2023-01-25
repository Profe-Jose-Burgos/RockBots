

import json
import requests
import datetime
from chatbot_respuesta import *
from funciones import *

class ultraChatBot():    
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['data']
        self.ultraAPIUrl = 'https://api.ultramsg.com/instance30106/'
        self.token = 'qwu8ilpa43lm6ysa'

   
    def send_requests(self, type, data):
        url = f"{self.ultraAPIUrl}{type}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatID, text):
        data = {"to" : chatID,
                "body" : text}  
        answer = self.send_requests('messages/chat', data)
        return answer
     
    def respuesta(self, chatID):
        message =self.dict_messages
        text = message['body'].split()
        Usuariomsg=text[0].lower() 
        answer=chatbot_respuesta(Usuariomsg) 
        return self.respuesta(chatID, answer)


    def Processingـincomingـmessages(self):
        if self.dict_messages != []:
            message =self.dict_messages
            text = message['body'].split()
            if not message['fromMe']:
                chatID  = message['from']
                return self.respuesta(chatID)

            else: return 'No válido'


