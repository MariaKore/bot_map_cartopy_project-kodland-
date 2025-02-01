import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    help_text = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Список команд\n"
        "/show_city <город> - Показать указанный город на карте\n"
        "/remember_city <город> [цвет] - Запомнить город и выбрать цвет маркера (по умолчанию красный)\n"
        "/show_my_cities - Показать все сохраненные города на карте"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split(maxsplit=1)[-1]
    if city_name:
        path = f"{city_name}_map.png"
        manager.create_graph(path, [(city_name, 'red')])
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите город.")

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    parts = message.text.split(maxsplit=2)
    city_name = parts[1]
    color = parts[2] if len(parts) > 2 else 'red'
    if manager.add_city(user_id, city_name, color):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен с маркером {color}!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    if cities:
        path = "my_cities_map.png"
        manager.create_graph(path, cities)
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "Вы не сохранили ни одного города.")

if __name__ == "__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
