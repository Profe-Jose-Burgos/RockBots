from flask import Flask, request, jsonify
from WHATSAPP import ultraChatBot
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = ultraChatBot(request.json)
        return bot.Processingـincomingـmessages()

@app.route('/', methods=['POST'])
def (respuestaAI):
    bot = request.json
    respuesta = chatbot_respuesta(bot)
    return respuesta.tolist()

if(__name__) == '__main__':
    app.run()














