import telebot
import firebase_admin
from firebase_admin import credentials, firestore
from threading import Thread
import time
import json
from datetime import datetime

import os

TG_BOT_API_TOKEN = os.getenv('TG_BOT_API_TOKEN')

cred = credentials.Certificate("secret.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

bot = telebot.TeleBot(
    TG_BOT_API_TOKEN, parse_mode=None)


def check_document_status(doc_ref, message, is_daily=False):
    while True:
        try:
            doc = doc_ref.get()
            if doc.exists:
                doc_data = doc.to_dict()
                status = doc_data.get("status", {})
                state = status.get("state")
                if state == "COMPLETED":
                    response_str = doc_data.get("response", "")
                    if response_str:
                        if is_daily:
                            try:
                                response_data = json.loads(response_str)
                                tasks = response_data.get("tasks", [])
                                formatted_response = "\n".join(
                                    [f"{idx+1}. {task['task']}: {task['description']}" for idx, task in enumerate(tasks)])
                                bot.reply_to(message, formatted_response)

                                users_ref = db.collection('users')
                                query = users_ref.where(
                                    'chatId', '==', str(message.chat.id))
                                docs = query.stream()

                                for doc in docs:
                                    uid = doc.id
                                    daily_ref = db.collection('users').document(uid).collection(
                                        'daily').document(datetime.now().isoformat())
                                    daily_ref.set(
                                        {"tasks": tasks, "timestamp": datetime.now()})
                                    break

                            except json.JSONDecodeError:
                                bot.reply_to(
                                    message, "There was an error parsing the response. Please try again.")
                                break
                        else:
                            bot.reply_to(
                                message, response_str)
                    else:
                        bot.reply_to(message, "No response received.")
                    break
                elif state == "ERROR":
                    error_message = status.get(
                        "error", "An unexpected error occurred.")
                    bot.reply_to(message, f"Error: {error_message}")
                    break
            else:
                bot.reply_to(message, "The document does not exist.")
                break
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")
            break
        time.sleep(5)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing? This bot is designed to help you quit smoking and deal with cravings. Feel free to write me anything anytime, I'll help you.")


uid_waiting_list = {} 


@bot.message_handler(commands=['uid'])
def prompt_for_uid(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Please enter your UID.")
    uid_waiting_list[chat_id] = True 


@bot.message_handler(func=lambda message: message.chat.id in uid_waiting_list)
def process_uid(message):
    if uid_waiting_list.get(message.chat.id):
        user_uid = message.text.strip()
        chat_id = message.chat.id
        user_ref = db.collection('users').document(user_uid)
        user_ref.set({"chatId": str(chat_id)}, merge=True)
        bot.reply_to(
            message, "Your chat ID has been successfully linked with UID: " + user_uid)


@bot.message_handler(commands=['daily'])
def send_daily(message):
    prompt = {
        'prompt': '''command: daily(provide only 3 random daily simple tasks in strict JSON format, without including charecters like \''' which are done for identation)
        Example JSON:
            {
            "tasks": [
                {
                "task": "Social Interaction",
                "description": "Try to meet with your family or friend to do something together. If meeting in person is not possible, consider an online meeting or a phone call."
                },
                {
                "task": "Deep Breathing Exercise",
                "description": "Practice deep breathing for a few minutes to help manage cravings and reduce stress."
                },
                {
                "task": "Self-Reward",
                "description": "Reward yourself with a small treat, like chocolate, candy, or a favorite fruit, to celebrate your progress."
                }
            ]
            }
        ''',
        'status': {
            'state': 'PENDING'
        },
    }
    doc_ref = db.collection('generate').document()
    doc_ref.set(prompt)

    Thread(target=check_document_status, args=(doc_ref, message, True)).start()


@bot.message_handler(func=lambda m: True)
def chat(message):
    prompt = {
        'prompt': message.text,
        'status': {
            'state': 'PENDING'
        }
    }
    doc_ref = db.collection('generate').document()
    doc_ref.set(prompt)

    Thread(target=check_document_status, args=(doc_ref, message)).start()


bot.polling()
