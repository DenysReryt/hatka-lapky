import telebot
from telebot import types
from config import settings
import crud
from app import app, last_message

token = settings.BOT_TOKEN

greeting = "Welcome to @testlapkybot! \nPlease choose one of the function \
    under the input field!"

bot = telebot.TeleBot(token)

def start_message(message, text):    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('📲 Chat')
    markup.add(button1)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)
    

@bot.message_handler(commands=['start'])
def handle_start(message):
    start_message(message=message, text=greeting)


@bot.message_handler(func=lambda message: message.text == '📲 Chat')
def handle_chat(message):
    markup_inline = types.InlineKeyboardMarkup()
    inlinebut1 = types.InlineKeyboardButton(text='Live chat', callback_data='chat')
    markup_inline.add(inlinebut1)
    
    bot.send_message(message.chat.id, 'Below you can start our support chat. After you click on "Live chat" button our manager will contact you as soon as possible.', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'chat':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        stop_chat = types.KeyboardButton('End Chat')
        markup_reply.add(stop_chat)
        
        bot.send_message(call.message.chat.id, text=f'Chat with manager has started', 
                         reply_markup=markup_reply)
        
        
        
@bot.message_handler(func=lambda message: message.text == 'End Chat')
def handle_stop_chat(message):
    user_id = message.from_user.id
    start_message(message=message, text='Chat has been ended. You can start a new chat by pressing "📲 Chat".')
    with app.app_context():
        chat = crud.get_chat_by_user_id(user_id=user_id)
        if chat:
            crud.stop_chat(user_id=user_id)      
           
    
    
@bot.message_handler(content_types=['text'])
def handle_chat_messages(message):
    user_id = message.from_user.id
    global last_message
    with app.app_context():
        chat = crud.get_chat_by_user_id(user_id=user_id)
        if chat:
            crud.update_chat(user_id=user_id, last_message=message.text)
        else:
            crud.create_chat(first_name=message.from_user.first_name, 
                             username=message.from_user.username, user_id=user_id, 
                             last_message=message.text)

    # bot.send_message(message.chat.id, text=last_message)

bot.polling(non_stop=True)
