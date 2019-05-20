import json
from flask import Flask, jsonify, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)


base_corpus = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]

chatbots = dict()


@app.route('/chatbot', methods=['POST'])
def chatbot_handler():
    json_data = json.loads(request.data.decode('utf-8'))
    user_id = json_data['user_id']
    text = json_data['text']

    if user_id in chatbots:
        chatbot = chatbots[user_id]
    else:
        chatbot = ChatBot(user_id)
        chatbots[user_id] = chatbot
        trainer = ListTrainer(chatbot)
        trainer.train(base_corpus)

    output = chatbot.get_response(text)
    return jsonify({'output': str(output)})
