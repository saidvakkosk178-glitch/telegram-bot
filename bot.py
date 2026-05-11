import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8508749402:AAHwsuywGvX3i3DoTLaLG-_2Bl2u7p9a878"
ADMIN_ID = 5456624192

bot = telebot.TeleBot(BOT_TOKEN)

user_waiting_input = {}
pending_questions = {}
last_selected_stars = {}

waiting_payment_screenshot = {}
last_price = {}
premium_months = {}

# -------------------- Главное меню ---------------------
def main_menu(chat_id, username):
    text = f"Привет, {username}! — Я твой личный помощник по покупке услуг, без лишних сложностей"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Популярные услуги 🔥", callback_data="popular"))
    keyboard.add(InlineKeyboardButton("💬 Помощь 🆘", callback_data="help"))
    keyboard.add(InlineKeyboardButton("⭐ Отзывы", url="https://t.me/joinchat/4tATMaLkcwZjMGE6"))

    bot.send_message(chat_id, text, reply_markup=keyboard)

# -------------------- START ---------------------
@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message.chat.id, message.from_user.username)

# -------------------- REPLY ---------------------
@bot.message_handler(commands=['reply'])
def reply_command(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        parts = message.text.split(' ', 2)

        user_id = int(parts[1])
        reply_text = parts[2]

        bot.send_message(
            user_id,
            f"🛡️ Ответ от поддержки:\n{reply_text}"
        )

        bot.send_message(
            ADMIN_ID,
            f"✅ Ответ отправлен пользователю {user_id}"
        )

    except Exception as e:
        bot.send_message(
            ADMIN_ID,
            f"❌ Ошибка: {e}"
        )

# -------------------- CALLBACKS ---------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    chat_id = call.message.chat.id

    # -------- Популярные услуги --------
    if call.data == "popular":

        keyboard = InlineKeyboardMarkup()

        keyboard.add(
            InlineKeyboardButton("Stars 🔥", callback_data="stars")
        )

        keyboard.add(
            InlineKeyboardButton("Premium 💎", callback_data="premium")
        )

        bot.send_message(
            chat_id,
            "Выберите услугу:",
            reply_markup=keyboard
        )

    # -------- STARS --------
    elif call.data == "stars":

        keyboard = InlineKeyboardMarkup()

        keyboard.row(
            InlineKeyboardButton("50 ⭐", callback_data="s_50"),
            InlineKeyboardButton("100 ⭐", callback_data="s_100"),
            InlineKeyboardButton("150 ⭐", callback_data="s_150"),
            InlineKeyboardButton("200 ⭐", callback_data="s_200")
        )

        keyboard.row(
            InlineKeyboardButton("250 ⭐", callback_data="s_250"),
            InlineKeyboardButton("300 ⭐", callback_data="s_300"),
            InlineKeyboardButton("350 ⭐", callback_data="s_350")
        )

        keyboard.row(
            InlineKeyboardButton("400 ⭐", callback_data="s_400"),
            InlineKeyboardButton("500 ⭐", callback_data="s_500"),
            InlineKeyboardButton("600 ⭐", callback_data="s_600")
        )

        keyboard.row(
            InlineKeyboardButton("700 ⭐", callback_data="s_700"),
            InlineKeyboardButton("800 ⭐", callback_data="s_800"),
            InlineKeyboardButton("900 ⭐", callback_data="s_900"),
            InlineKeyboardButton("1000 ⭐", callback_data="s_1000")
        )

        keyboard.add(
            InlineKeyboardButton(
                "Указать своё количество ⭐",
                callback_data="custom"
            )
        )

        keyboard.add(
            InlineKeyboardButton(
                "⬅️ Назад",
                callback_data="popular"
            )
        )

        bot.send_message(
            chat_id,
            "⭐ Выберите пакет:",
            reply_markup=keyboard
        )

    elif call.data.startswith("s_"):

        stars = int(call.data.split("_")[1])

        last_selected_stars[chat_id] = stars

        # ЦЕНА 240
        price = stars * 240

        last_price[chat_id] = price

        waiting_payment_screenshot[chat_id] = True

        bot.send_message(
            chat_id,
f"""💳 Чтобы совершить заказ оплатите по реквизитам:

💳 Номер карты:
`5614681713813289`

👤 Получатель:
ABDULBOSITOV MUHAMMADALI

💰 Сумма платежа:
`{price} сум`

📸 После оплаты пришлите скриншот оплаты
""",
            parse_mode="Markdown"
        )

    elif call.data == "custom":

        user_waiting_input[chat_id] = True

        bot.send_message(
            chat_id,
            "Введите количество ⭐ (минимум 50):"
        )

    # -------- PREMIUM --------
    elif call.data == "premium":

        keyboard = InlineKeyboardMarkup()

        keyboard.add(
            InlineKeyboardButton(
                "1 месяц — 40.000",
                callback_data="p_1"
            )
        )

        keyboard.add(
            InlineKeyboardButton(
                "3 месяца — 162.000",
                callback_data="p_3"
            )
        )

        keyboard.add(
            InlineKeyboardButton(
                "6 месяцев — 222.000",
                callback_data="p_6"
            )
        )

        keyboard.add(
            InlineKeyboardButton(
                "12 месяцев — 378.000",
                callback_data="p_12"
            )
        )

        keyboard.add(
            InlineKeyboardButton(
                "⬅️ Назад",
                callback_data="popular"
            )
        )

        bot.send_message(
            chat_id,
            "💎 Выберите тариф:",
            reply_markup=keyboard
        )

    elif call.data.startswith("p_"):

        months = int(call.data.split("_")[1])

        premium_months[chat_id] = months

        prices = {
            1: 40000,
            3: 162000,
            6: 222000,
            12: 378000
        }

        price = prices[months]

        last_price[chat_id] = price

        waiting_payment_screenshot[chat_id] = True

        bot.send_message(
            chat_id,
f"""💳 Чтобы совершить заказ оплатите по реквизитам:

💳 Номер карты:
`5614681713813289`

👤 Получатель:
ABDULBOSITOV MUHAMMADALI

💰 Сумма платежа:
`{price} сум`

📸 После оплаты пришлите скриншот оплаты
""",
            parse_mode="Markdown"
        )

    # -------- HELP --------
    elif call.data == "help":

        pending_questions[chat_id] = call.from_user.username

        bot.send_message(
            chat_id,
            "Напишите свой вопрос:"
        )

# -------------------- CUSTOM STARS ---------------------
@bot.message_handler(func=lambda m: m.chat.id in user_waiting_input)
def custom_handler(m):

    chat_id = m.chat.id

    try:

        stars = int(m.text)

        if stars < 50:

            bot.send_message(
                chat_id,
                "❌ Минимум 50 ⭐"
            )

            return

        last_selected_stars[chat_id] = stars

        # ЦЕНА 240
        price = stars * 240

        last_price[chat_id] = price

        waiting_payment_screenshot[chat_id] = True

        bot.send_message(
            chat_id,
f"""💳 Чтобы совершить заказ оплатите по реквизитам:

💳 Номер карты:
`5614681713813289`

👤 Получатель:
ABDULBOSITOV MUHAMMADALI

💰 Сумма платежа:
`{price} сум`

📸 После оплаты пришлите скриншот оплаты
""",
            parse_mode="Markdown"
        )

    except:

        bot.send_message(
            chat_id,
            "❌ Введите число!"
        )

    finally:

        user_waiting_input.pop(chat_id, None)

# -------------------- SCREENSHOT ---------------------
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):

    chat_id = message.chat.id

    if chat_id not in waiting_payment_screenshot:
        return

    file_id = message.photo[-1].file_id

    username = message.from_user.username
    user_id = message.from_user.id

    stars = last_selected_stars.get(chat_id)
    months = premium_months.get(chat_id)

    text = f"📦 Новый заказ от {username} ({user_id})\n"

    if stars:
        text += f"⭐ Stars: {stars}\n"

    if months:
        text += f"💎 Premium: {months} мес\n"

    bot.send_photo(
        ADMIN_ID,
        file_id,
        caption=text
    )

    bot.send_message(
        chat_id,
        "🎉 Спасибо за ваш заказ!\nВ скором времени владелец выполнит ваш заказ."
    )

    waiting_payment_screenshot.pop(chat_id, None)

# -------------------- QUESTIONS ---------------------
@bot.message_handler(func=lambda m: m.chat.id in pending_questions)
def handle_question(m):

    username = pending_questions[m.chat.id]

    bot.send_message(
        m.chat.id,
        "Спасибо за ваш вопрос, ваш вопрос отправлен Администратору, в скором времени вам ответят 💬"
    )

    bot.send_message(
        ADMIN_ID,
        f"❗ Вопрос от {username} ({m.chat.id}): {m.text}"
    )

    pending_questions.pop(m.chat.id, None)

# -------------------- START BOT ---------------------
print("Бот запущен...")

bot.polling(none_stop=True)
