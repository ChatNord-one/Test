import telebot
from telebot import types
import re

TOKEN = "8322158637:AAFY2taPDU5Cs_yXjM4CAmPd_BwLu5ZLSDE"
bot = telebot.TeleBot(TOKEN)

# ❌ очищаємо старі команди
bot.delete_my_commands()

# ✅ додаємо лише /start
bot.set_my_commands([
    telebot.types.BotCommand("start", "Почати роботу з ботом")
])

# Дані користувачів
user_data = {}      # тимчасове збереження під час реєстрації
registered_users = set()  # хто вже зареєстрований

# --- РЕЄСТРАЦІЯ ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id in registered_users:
        bot.reply_to(message, "✅ Ти вже зареєстрований! Можеш користуватись меню нижче 👇")
        show_main_menu(message)
        return

    bot.reply_to(message, "👋 Привіт! Введи своє ім’я:")
    user_data[user_id] = {"step": "name"}


@bot.message_handler(func=lambda message: True)
def handle_registration(message):
    user_id = message.chat.id
    text = message.text.strip()

    # якщо користувач не почав /start
    if user_id not in user_data and user_id not in registered_users:
        bot.reply_to(message, "❗ Спочатку напиши /start, щоб почати реєстрацію")
        return

    # якщо користувач уже зареєстрований — працює основне меню
    if user_id in registered_users:
        handle_main_menu(message)
        return

    step = user_data[user_id]["step"]

    # === 1. ІМ'Я ===
    if step == "name":
        if len(text) < 2:
            bot.reply_to(message, "❌ Ім’я занадто коротке. Спробуй ще раз.")
            return
        user_data[user_id]["name"] = text
        user_data[user_id]["step"] = "email"
        bot.reply_to(message, "📧 Добре, тепер введи свій email:")

    # === 2. EMAIL ===
    elif step == "email":
        if "@" not in text or "." not in text:
            bot.reply_to(message, "❌ Це не схоже на email. Напиши правильну адресу.")
            return
        user_data[user_id]["email"] = text
        user_data[user_id]["step"] = "password"
        bot.reply_to(message, "🔑 Тепер введи пароль (лише англійські букви та цифри):")

    # === 3. ПАРОЛЬ ===
    elif step == "password":
        # перевірка, що пароль англійською (мін. 4 символи)
        if not re.match(r'^[A-Za-z0-9!@#$%^&*()_+=-]{4,}$', text):
            bot.reply_to(message, "❌ Пароль має бути лише англійською (мін. 4 символи).")
            return

        user_data[user_id]["password"] = text
        name = user_data[user_id]["name"]
        email = user_data[user_id]["email"]
        password = user_data[user_id]["password"]

        # зберігаємо у файл
        with open("data.txt", "a", encoding="utf-8") as f:
            f.write(f"{name} | {email} | {password}\n")

        registered_users.add(user_id)
        user_data.pop(user_id)

        bot.reply_to(message, f"✅ Дякую, {name}! Ти успішно зареєструвався 🎉")
        show_main_menu(message)


# --- ГОЛОВНЕ МЕНЮ ---
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("/info", "/Hellp", "/Settings")
    markup.add("Привіт", "Як справи?", "Пака")
    bot.send_message(message.chat.id, "Оберіть команду 👇", reply_markup=markup)


# --- ОСНОВНА ЛОГІКА ---
def handle_main_menu(message):
    text = message.text

    if text == "/info":
        bot.reply_to(message, "📘 Це інформація про бота. Можна додавати шпаргалки 😎")
    elif text == "/Hellp":
        bot.reply_to(message, "- /info\n- /Hellp\n- /Settings\n- /start")
    elif text == "/Settings":
        bot.reply_to(message, "⚙️ Налаштування поки в розробці.")
    elif text.lower() in ["привіт", "hello"]:
        bot.reply_to(message, "👋 Привіт, друже!")
    elif text.lower() in ["як справи?", "як справи", "how are you"]:
        bot.reply_to(message, "😊 Все чудово! А в тебе?")
    elif text.lower() in ["пака", "bye"]:
        bot.reply_to(message, "👋 Бувай!")
    else:
        bot.reply_to(message, f"❌ '{text}' — це не команда. Вибери зі списку нижче.")


print("✅ Бот запущений!")
bot.infinity_polling()
