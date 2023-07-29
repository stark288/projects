from flask import Flask, request, jsonify, render_template, redirect, send_from_directory

import pickle
import numpy as np
import json
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
import nltk
import random
import re

app = Flask(__name__)

@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/static/imgs/<path:path>')
def send_imgs(path):
    return send_from_directory('static/imgs', path)

# Load necessary data and models
lemmatizer = WordNetLemmatizer()
intents_file = json.loads(open('E:\whole_dataset1.json').read())
lem_words = pickle.load(open('D:\modfiles\lem_words.pkl', 'rb'))
classes = pickle.load(open('D:\modfiles\classes.pkl', 'rb'))
bot_model = load_model('D:\modfiles\chatbot_model1.h5')


def cleaning(text):
    words = nltk.word_tokenize(text)
    words = [lemmatizer.lemmatize(word.lower()) for word in words]
    return words


def bag_of_words(text, words, show_details=True):
    sentence_words = cleaning(text)
    bag_of_words = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag_of_words[i] = 1
    return np.array(bag_of_words)


def class_prediction(sentence, model):
    p = bag_of_words(sentence, lem_words, show_details=False)
    result = bot_model.predict(np.array([p]))[0]
    ER_THRESHOLD = 0.30
    f_results = [[i, r] for i, r in enumerate(result) if r > ER_THRESHOLD]
    f_results.sort(key=lambda x: x[1], reverse=True)
    intent_prob_list = []
    for i in f_results:
        intent_prob_list.append(
            {"intent": classes[i[0]], "probability": str(i[1])})
    return intent_prob_list


def get_bot_response(ints, intents):
    tag = ints[0]['intent']
    intents_list = intents['intents']
    for intent in intents_list:
        if intent['tag'] == tag:
            result = random.choice(intent['responses'])
            break
    return result


def process_user_input(user_input):
    # Check if the user input contains keywords related to booking appointments
    if re.search(r'\b(book|make|schedule)\b.*\bappointment\b', user_input, re.IGNORECASE):
        # Redirect the user to the appointment page
        return redirect_to_appointment_page()
    else:
        # Handle other user inputs
        return handle_other_input()


def redirect_to_appointment_page():
    # Here, you can implement the logic to redirect the user to your website's appointment page
    # For example, you can use a web framework like Flask or Django to handle the routing
    # You can also use a library like requests to programmatically open the page in a browser
    # Replace the URL with your own appointment page URL
    appointment_page_url = "http://localhost/edoc-doctor-appointment-system-main/"
    # Redirect the user to the appointment page
    return f"Sure! Please visit {appointment_page_url} to book an appointment."


def handle_other_input():
    # Handle other user inputs or provide a default response
    return "I'm sorry, I couldn't understand your request."


@app.route('/get_bot_response', methods=['POST'])
def get_bot_response_route():
    data = request.get_json()
    message = data['message']
    ints = class_prediction(message, bot_model)

    # Check if the user's intent is related to making or booking an appointment
    appointment_intents = ['make_appointment', 'book_appointment']
    if ints[0]['intent'] in appointment_intents:
        return redirect_to_appointment_page()

    response = get_bot_response(ints, intents_file)
    return jsonify(response)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
