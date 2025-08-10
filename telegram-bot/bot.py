import os
import re
from PIL import Image, ImageDraw, ImageFont
from telebot import TeleBot, types
from io import BytesIO
from datetime import datetime

# Настройки бота
TOKEN = '7868525280:AAHE1bTQvsi6_viEXoibfZVTRVWXnnILiAw'  # Обновленный токен
ADMIN_ID = 1296547505  # ID главного администратора
ALLOWED_USERS = {6033232568,877680990,6608918690,7474635230}  # Начальный набор разрешенных пользователей

# Настройки водяного знака
WATERMARK_TEXT = "ФЕЙК СКРИН @ScreenFakeShot_bot"  # Текст водяного знака
WATERMARK_COLOR = "#FFFFFF"  # Цвет в формате HEX
WATERMARK_OPACITY = 160  # Прозрачность (0-255, где 0 - полностью прозрачный)
WATERMARK_FONT_SIZE = 40  # Размер шрифта
WATERMARK_ANGLE = -30  # Угол наклона в градусах (положительный - вправо)
WATERMARK_HORIZONTAL_SPACING = 650  # Расстояние между знаками по горизонтали
WATERMARK_VERTICAL_SPACING = 75  # Расстояние между знаками по вертикали
WATERMARK_FONT_PATH = "sb-sans-text-medium.ttf"  # Путь к шрифту

# Базовый путь к файлам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------- НАСТРОЙКИ СБЕРБАНКА -----------------
SBER_TEMPLATE_1 = "sber1.png"  # Для 5 строк (с тратами)
SBER_TEMPLATE_2 = "sber2.png"  # Для 4 строк (без трат)

# Настройки для первого ФИО (капс)
SBER_NAME1_X = 228
SBER_NAME1_Y = 1266
SBER_NAME1_FONT_PATH = os.path.join(BASE_DIR, "sb-sans-text-medium.ttf")
SBER_NAME1_FONT_SIZE = 44
SBER_NAME1_COLOR = "#FFFFFF"

# Настройки для второго ФИО
SBER_NAME2_X = 228
SBER_NAME2_Y = 1615
SBER_NAME2_FONT_PATH = os.path.join(BASE_DIR, "sb-sans-text-medium.ttf")
SBER_NAME2_FONT_SIZE = 44
SBER_NAME2_COLOR = "#FFFFFF"

# Настройки для сумм
SBER_AMOUNT_X = 1065
SBER_AMOUNT_OFFSET = -2  # Смещение суммы относительно ФИО
SBER_AMOUNT_FONT_PATH = os.path.join(BASE_DIR, "sb-sans-text-medium.ttf")
SBER_AMOUNT_FONT_SIZE = 50
SBER_AMOUNT_COLOR = "#428D3B"

# Настройки для трат
SBER_EXPENSES_X = 1065
SBER_EXPENSES_Y = 1111
SBER_EXPENSES_Y2 = 1460  # Вторая позиция для трат
SBER_EXPENSES_FONT_PATH = os.path.join(BASE_DIR, "sb-sans-text-medium.ttf")
SBER_EXPENSES_FONT_SIZE = 50
SBER_EXPENSES_COLOR = "#888888"

# ----------------- НАСТРОЙКИ ТИНЬКОФФ БАНКА -----------------
TBANK_TEMPLATE_1 = "tb1.png"  # Для 11 строк (с тратами)
TBANK_TEMPLATE_2 = "tb2.png"  # Для 10 строк (без трат)

# Настройки для ФИО
TBANK_NAME_X = 217
TBANK_NAME_Y_START = 627
TBANK_NAME_Y_STEP = 316
TBANK_NAME_FONT_PATH = os.path.join(BASE_DIR, "blinkmacsystemfont-medium.ttf")
TBANK_NAME_FONT_SIZE = 51
TBANK_NAME_COLOR = "#F6F7F8"

# Настройки для сумм
TBANK_AMOUNT_X = 1087
TBANK_AMOUNT_FONT_PATH = os.path.join(BASE_DIR, "blinkmacsystemfont-regular.ttf")
TBANK_AMOUNT_FONT_SIZE = 50.9
TBANK_AMOUNT_COLOR = "#00B92D"

# Настройки для знака "+" в Тинькофф
TBANK_PLUS_SIGN_FONT_PATH = os.path.join(BASE_DIR, "blinkmacsystemfont-regular.ttf")
TBANK_PLUS_SIGN_FONT_SIZE = 52
TBANK_PLUS_SIGN_COLOR = "#00B92D"
TBANK_PLUS_SIGN_X_OFFSET = -21  # Смещение по X относительно суммы
TBANK_PLUS_SIGN_Y_OFFSET = -1  # Смещение по Y относительно суммы

# Настройки для знака "-" в Тинькофф (для трат)
TBANK_MINUS_SIGN_FONT_PATH = os.path.join(BASE_DIR, "Raleway-Light.ttf")
TBANK_MINUS_SIGN_FONT_SIZE = 91.4
TBANK_MINUS_SIGN_COLOR = "#606062"
TBANK_MINUS_SIGN_X_OFFSET = -25  # Смещение по X относительно суммы
TBANK_MINUS_SIGN_Y_OFFSET = -25  # Смещение по Y относительно суммы

# Настройки для трат (5 позиций)
TBANK_EXPENSES_X = 1087
TBANK_EXPENSES_Y_POSITIONS = [465, 465 + 316, 465 + 316 + 316, 465 + 316 + 316 + 316, 465 + 316 + 316 + 316 + 316]
TBANK_EXPENSES_FONT_PATH = os.path.join(BASE_DIR, "blinkmacsystemfont-regular.ttf")
TBANK_EXPENSES_FONT_SIZE = 50.9
TBANK_EXPENSES_COLOR = "#606062"

# ----------------- НАСТРОЙКИ OZON -----------------
OZON_TEMPLATE = "ozon.png"

# Настройки для ФИО
OZON_NAME_X = 229
OZON_NAME_Y_START = 595
OZON_NAME_Y_STEP = 278
OZON_NAME_FONT_PATH = os.path.join(BASE_DIR, "blinkmacsystemfont-regular.ttf")
OZON_NAME_FONT_SIZE = 49
OZON_NAME_COLOR = "#F5F7FA"

# Настройки для сумм
OZON_AMOUNT_X = 1092
OZON_AMOUNT_FONT_PATH = os.path.join(BASE_DIR, "ozonfont_regular.ttf")
OZON_AMOUNT_FONT_SIZE = 48
OZON_AMOUNT_COLOR = "#1DED62"

# Настройки для знака "+" в Ozon
OZON_PLUS_SIGN_FONT_PATH = os.path.join(BASE_DIR, "blinkmacsystemfont-regular.ttf")
OZON_PLUS_SIGN_FONT_SIZE = 39
OZON_PLUS_SIGN_COLOR = "#1DED62"
OZON_PLUS_SIGN_X_OFFSET = -21  # Смещение по X относительно суммы
OZON_PLUS_SIGN_Y_OFFSET = 3  # Смещение по Y относительно суммы

# Настройки для 6-й строки в Ozon (отдельные настройки)
OZON_ROW6_NAME_Y = 581 + 5 * 277  # Позиция Y для 6-й строки (можно изменить)
OZON_ROW6_AMOUNT_Y = OZON_ROW6_NAME_Y  # Позиция Y для суммы в 6-й строке

# ----------------- НАСТРОЙКИ АЛЬФА БАНКА -----------------
ALPHA_TEMPLATE = "alpha.png"

# Настройки для ФИО
ALPHA_NAME_X = 253
ALPHA_NAME_Y_START = 938
ALPHA_NAME_Y_STEP = 315
ALPHA_NAME_FONT_PATH = os.path.join(BASE_DIR, "blinkmacsystemfont-medium.ttf")
ALPHA_NAME_FONT_SIZE = 52
ALPHA_NAME_COLOR = "#FFFFFF"

# Настройки для сумм
ALPHA_AMOUNT_X = 1061
ALPHA_AMOUNT_FONT_PATH = os.path.join(BASE_DIR, "blinkmacsystemfont-medium.ttf")
ALPHA_AMOUNT_FONT_SIZE = 52
ALPHA_AMOUNT_COLOR = "#4BA269"

# Настройки для знака "+" в Альфа
ALPHA_PLUS_SIGN_FONT_PATH = os.path.join(BASE_DIR, "blinkmacsystemfont-medium.ttf")
ALPHA_PLUS_SIGN_FONT_SIZE = ALPHA_AMOUNT_FONT_SIZE
ALPHA_PLUS_SIGN_COLOR = ALPHA_AMOUNT_COLOR
ALPHA_PLUS_SIGN_X_OFFSET = -25  # Смещение по X относительно суммы
ALPHA_PLUS_SIGN_Y_OFFSET = 0  # Смещение по Y относительно суммы

# Настройки для даты (3 позиции)
ALPHA_DATE_POSITIONS = [
    (245, 818),  # Первая позиция
    (245, 1133),  # Вторая позиция
    (245, 1448)  # Третья позиция
]
ALPHA_DATE_FONT_PATH = os.path.join(BASE_DIR, "blinkmacsystemfont-black.ttf")
ALPHA_DATE_FONT_SIZE = 33
ALPHA_DATE_COLOR = "#87878C"

# Создаем экземпляр бота
bot = TeleBot(TOKEN)


# Главное меню
def create_main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('СБЕР ✅')
    btn2 = types.KeyboardButton('ТБАНК 📒')
    btn3 = types.KeyboardButton('ОЗОН 🔵')
    btn4 = types.KeyboardButton('АЛЬФА 🅰️')

    if user_id == ADMIN_ID:
        btn5 = types.KeyboardButton('Добавить пользователя 👨🏻‍💻')
        btn6 = types.KeyboardButton('Удалить пользователя ❌')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    else:
        markup.add(btn1, btn2, btn3, btn4)
    return markup


# Проверка доступа пользователя
def is_user_allowed(user_id):
    return user_id in ALLOWED_USERS


# Отправка изображения как файла без сжатия
def send_image_as_file(chat_id, image, caption=None, watermark=False):
    if watermark:
        # Создаем временное изображение для работы с прозрачностью
        watermark_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)

        try:
            font = ImageFont.truetype(WATERMARK_FONT_PATH, WATERMARK_FONT_SIZE)
        except:
            font = ImageFont.load_default()

        # Разбираем HEX-цвет и добавляем прозрачность
        color = WATERMARK_COLOR.lstrip('#')
        rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        rgba = rgb + (WATERMARK_OPACITY,)

        # Получаем размеры текста с помощью textbbox
        bbox = draw.textbbox((0, 0), WATERMARK_TEXT, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Рисуем водяные знаки по всему изображению
        width, height = image.size
        for y in range(-height, height * 2, WATERMARK_VERTICAL_SPACING):
            for x in range(-width, width * 2, WATERMARK_HORIZONTAL_SPACING):
                # Создаем временное изображение для поворота
                text_layer = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
                text_draw = ImageDraw.Draw(text_layer)
                text_draw.text((0, 0), WATERMARK_TEXT, font=font, fill=rgba)

                # Поворачиваем текст
                rotated = text_layer.rotate(WATERMARK_ANGLE, expand=1)

                # Накладываем повернутый текст
                watermark_layer.paste(rotated, (x, y), rotated)

        # Накладываем водяной знак на оригинальное изображение
        image = Image.alpha_composite(image.convert('RGBA'), watermark_layer).convert('RGB')

    # Всегда отправляем уведомление администратору, если это не он сам
    if chat_id != ADMIN_ID:
        try:
            user = bot.get_chat(chat_id)
            username = f"@{user.username}" if user.username else "нет username"
            admin_message = f"Пользователь {username} (ID: {chat_id}) создал скриншот"

            # Создаем копию изображения для отправки администратору
            admin_bio = BytesIO()
            admin_bio.name = 'screenshot.png'
            image.save(admin_bio, 'PNG', quality=100)
            admin_bio.seek(0)

            bot.send_document(ADMIN_ID, admin_bio, caption=admin_message)
        except Exception as e:
            print(f"Ошибка при отправке уведомления администратору: {e}")

    bio = BytesIO()
    bio.name = 'result.png'
    image.save(bio, 'PNG', quality=100)
    bio.seek(0)
    bot.send_document(chat_id, bio, caption=caption)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите банк:",
                     reply_markup=create_main_menu(message.from_user.id))


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id

    if message.text == 'СБЕР ✅':
        response = """✏️ Отправьте данные в формате:
ФИО 1
Сумма 1
ФИО 2
Сумма 2
Траты (можно оставить пустым)

Пример:
<code>Анастасия Андреевна З.
8
Анастасия Андреевна З.
29
498,98</code>"""
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        bot.register_next_step_handler(message, process_sber_data)

    elif message.text == 'ТБАНК 📒':
        response = """✏️ Отправьте данные в формате:
ФИО 1
Сумма 1
ФИО 2
Сумма 2
ФИО 3
Сумма 3
ФИО 4
Сумма 4
ФИО 5
Сумма 5
Траты (можно оставить пустым)

Пример:
<code>Виктор Ч.
150
Михаил Л.
70
Никита А.
116
Егор И.
2 430
Кирилл Е.
55
800</code>"""
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        bot.register_next_step_handler(message, process_tb_data)

    elif message.text == 'ОЗОН 🔵':
        response = """✏️ Отправьте данные в формате:
ФИО 1
Сумма 1
ФИО 2
Сумма 2
ФИО 3
Сумма 3
ФИО 4
Сумма 4
ФИО 5
Сумма 5
ФИО 6
Сумма 6

Пример:
<code>София Романовна Л.
30
Павел Юрьевич П.
10
Аюна Сергеевна Б.
10
Андрей Сергеевич Л.
50
Никита Евгеньевич К.
50
Роман Рустемович Н.
25</code>"""
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        bot.register_next_step_handler(message, process_ozon_data)

    elif message.text == 'АЛЬФА 🅰️':
        response = """✏️ Отправьте данные в формате:
ФИО 1
Сумма 1
ФИО 2
Сумма 2
ФИО 3
Сумма 3

Пример:
<code>Ярослав Т.
10
Максим И.
10
Егор И.
10</code>"""  # Обновленный пример
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        bot.register_next_step_handler(message, process_alpha_data)

    elif message.text == 'Добавить пользователя 👨🏻‍💻' and user_id == ADMIN_ID:
        bot.send_message(message.chat.id, "Отправьте ID пользователя, которого хотите добавить:")
        bot.register_next_step_handler(message, add_user)

    elif message.text == 'Удалить пользователя ❌' and user_id == ADMIN_ID:
        bot.send_message(message.chat.id, "Отправьте ID пользователя, которого хотите удалить:")
        bot.register_next_step_handler(message, remove_user)


# Обработка данных для Сбербанка
def process_sber_data(message):
    try:
        data = [line.strip() for line in message.text.split('\n') if line.strip()]

        if len(data) not in [4, 5]:
            bot.send_message(message.chat.id,
                             "Неверный формат данных. Пожалуйста, отправьте данные в указанном формате.")
            return

        # Выбираем шаблон в зависимости от количества строк
        template = SBER_TEMPLATE_1 if len(data) == 5 else SBER_TEMPLATE_2

        # Открываем шаблон
        try:
            img = Image.open(template)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Шаблон не найден. Обратитесь к администратору.")
            return

        draw = ImageDraw.Draw(img)

        # Загружаем шрифты
        try:
            name1_font = ImageFont.truetype(SBER_NAME1_FONT_PATH, SBER_NAME1_FONT_SIZE)
        except:
            name1_font = ImageFont.load_default()

        try:
            name2_font = ImageFont.truetype(SBER_NAME2_FONT_PATH, SBER_NAME2_FONT_SIZE)
        except:
            name2_font = ImageFont.load_default()

        try:
            amount_font = ImageFont.truetype(SBER_AMOUNT_FONT_PATH, SBER_AMOUNT_FONT_SIZE)
        except:
            amount_font = ImageFont.load_default()

        # Обрабатываем первое ФИО (в верхнем регистре)
        name1 = data[0].upper()
        amount1 = format_amount(data[1])

        # Обрабатываем второе ФИО
        name2 = data[2]
        amount2 = format_amount(data[3])

        # Рисуем первое ФИО и сумму
        draw.text((SBER_NAME1_X, SBER_NAME1_Y), name1, font=name1_font, fill=SBER_NAME1_COLOR)
        bbox = draw.textbbox((0, 0), f"+{amount1}", font=amount_font)
        amount_width = bbox[2] - bbox[0]
        draw.text((SBER_AMOUNT_X - amount_width, SBER_NAME1_Y + SBER_AMOUNT_OFFSET),
                  f"+{amount1}", font=amount_font, fill=SBER_AMOUNT_COLOR)

        # Рисуем второе ФИО и сумму
        draw.text((SBER_NAME2_X, SBER_NAME2_Y), name2, font=name2_font, fill=SBER_NAME2_COLOR)
        bbox = draw.textbbox((0, 0), f"+{amount2}", font=amount_font)
        amount_width = bbox[2] - bbox[0]
        draw.text((SBER_AMOUNT_X - amount_width, SBER_NAME2_Y + SBER_AMOUNT_OFFSET),
                  f"+{amount2}", font=amount_font, fill=SBER_AMOUNT_COLOR)

        # Если есть траты
        if len(data) == 5:
            expenses = format_amount(data[4])
            try:
                expenses_font = ImageFont.truetype(SBER_EXPENSES_FONT_PATH, SBER_EXPENSES_FONT_SIZE)
            except:
                expenses_font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), expenses, font=expenses_font)  # Убрали минус перед expenses
            expenses_width = bbox[2] - bbox[0]
            # Рисуем траты дважды - на двух разных позициях
            draw.text((SBER_EXPENSES_X - expenses_width, SBER_EXPENSES_Y),
                      expenses, font=expenses_font, fill=SBER_EXPENSES_COLOR)  # Убрали минус
            draw.text((SBER_EXPENSES_X - expenses_width, SBER_EXPENSES_Y2),
                      expenses, font=expenses_font, fill=SBER_EXPENSES_COLOR)  # Убрали минус

        # Отправляем изображение с водяным знаком, если пользователь не авторизован
        send_image_as_file(message.chat.id, img, watermark=not is_user_allowed(message.from_user.id))

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


# Обработка данных для Тинькофф Банка
def process_tb_data(message):
    try:
        data = [line.strip() for line in message.text.split('\n') if line.strip()]

        if len(data) not in [10, 11]:
            bot.send_message(message.chat.id,
                             "Неверный формат данных. Пожалуйста, отправьте данные в указанном формате.")
            return

        # Выбираем шаблон
        template = TBANK_TEMPLATE_1 if len(data) == 11 else TBANK_TEMPLATE_2

        try:
            img = Image.open(template)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Шаблон не найден. Обратитесь к администратору.")
            return

        draw = ImageDraw.Draw(img)

        # Загружаем шрифты
        try:
            name_font = ImageFont.truetype(TBANK_NAME_FONT_PATH, TBANK_NAME_FONT_SIZE)
        except:
            name_font = ImageFont.load_default()

        try:
            amount_font = ImageFont.truetype(TBANK_AMOUNT_FONT_PATH, TBANK_AMOUNT_FONT_SIZE)
        except:
            amount_font = ImageFont.load_default()

        try:
            plus_font = ImageFont.truetype(TBANK_PLUS_SIGN_FONT_PATH, TBANK_PLUS_SIGN_FONT_SIZE)
        except:
            plus_font = ImageFont.load_default()

        try:
            minus_font = ImageFont.truetype(TBANK_MINUS_SIGN_FONT_PATH, TBANK_MINUS_SIGN_FONT_SIZE)
        except:
            minus_font = ImageFont.load_default()

        # Обрабатываем ФИО и суммы
        for i in range(0, min(10, len(data)), 2):
            name = data[i]
            amount = format_amount(data[i + 1])
            y = TBANK_NAME_Y_START + (i // 2) * TBANK_NAME_Y_STEP

            draw.text((TBANK_NAME_X, y), name, font=name_font, fill=TBANK_NAME_COLOR)
            bbox = draw.textbbox((0, 0), amount, font=amount_font)
            amount_width = bbox[2] - bbox[0]

            # Рисуем сумму
            draw.text((TBANK_AMOUNT_X - amount_width, y),
                      amount, font=amount_font, fill=TBANK_AMOUNT_COLOR)

            # Рисуем знак "+" отдельно с настройками шрифта и смещения
            plus_x = TBANK_AMOUNT_X - amount_width - 10 + TBANK_PLUS_SIGN_X_OFFSET
            plus_y = y + TBANK_PLUS_SIGN_Y_OFFSET
            draw.text((plus_x, plus_y), "+", font=plus_font, fill=TBANK_PLUS_SIGN_COLOR)

        # Обрабатываем траты (5 раз на разных Y)
        if len(data) == 11:
            expenses = format_amount(data[10])
            try:
                expenses_font = ImageFont.truetype(TBANK_EXPENSES_FONT_PATH, TBANK_EXPENSES_FONT_SIZE)
            except:
                expenses_font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), expenses, font=expenses_font)
            expenses_width = bbox[2] - bbox[0]

            for y in TBANK_EXPENSES_Y_POSITIONS:
                # Рисуем сумму трат
                draw.text((TBANK_EXPENSES_X - expenses_width, y),
                          expenses, font=expenses_font, fill=TBANK_EXPENSES_COLOR)

                # Рисуем знак "-" отдельно с настройками шрифта и смещения
                minus_x = TBANK_EXPENSES_X - expenses_width - 10 + TBANK_MINUS_SIGN_X_OFFSET
                minus_y = y + TBANK_MINUS_SIGN_Y_OFFSET
                draw.text((minus_x, minus_y), "-", font=minus_font, fill=TBANK_MINUS_SIGN_COLOR)

        # Отправляем изображение с водяным знаком, если пользователь не авторизован
        send_image_as_file(message.chat.id, img, watermark=not is_user_allowed(message.from_user.id))

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


# Обработка данных для Ozon
def process_ozon_data(message):
    try:
        data = [line.strip() for line in message.text.split('\n') if line.strip()]

        if len(data) != 12:
            bot.send_message(message.chat.id,
                             "Неверный формат данных. Пожалуйста, отправьте 12 строк (6 ФИО и 6 сумм).")
            return

        template = OZON_TEMPLATE

        try:
            img = Image.open(template)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Шаблон не найден. Обратитесь к администратору.")
            return

        draw = ImageDraw.Draw(img)

        # Загружаем шрифты
        try:
            name_font = ImageFont.truetype(OZON_NAME_FONT_PATH, OZON_NAME_FONT_SIZE)
        except:
            name_font = ImageFont.load_default()

        try:
            amount_font = ImageFont.truetype(OZON_AMOUNT_FONT_PATH, OZON_AMOUNT_FONT_SIZE)
        except:
            amount_font = ImageFont.load_default()

        try:
            plus_font = ImageFont.truetype(OZON_PLUS_SIGN_FONT_PATH, OZON_PLUS_SIGN_FONT_SIZE)
        except:
            plus_font = ImageFont.load_default()

        for i in range(0, 12, 2):
            if i + 1 >= len(data):
                break

            name = data[i]
            amount = format_amount(data[i + 1])

            # Определяем позицию Y в зависимости от строки
            if i == 10:  # 6-я строка (индексы 10 и 11)
                y_name = OZON_ROW6_NAME_Y
                y_amount = OZON_ROW6_AMOUNT_Y
            else:
                y_name = OZON_NAME_Y_START + (i // 2) * OZON_NAME_Y_STEP
                y_amount = y_name

            draw.text((OZON_NAME_X, y_name), name, font=name_font, fill=OZON_NAME_COLOR)
            bbox = draw.textbbox((0, 0), amount, font=amount_font)
            amount_width = bbox[2] - bbox[0]

            # Рисуем сумму
            draw.text((OZON_AMOUNT_X - amount_width, y_amount),
                      amount, font=amount_font, fill=OZON_AMOUNT_COLOR)

            # Рисуем знак "+" отдельно с настройками шрифта и смещения
            plus_x = OZON_AMOUNT_X - amount_width - 10 + OZON_PLUS_SIGN_X_OFFSET
            plus_y = y_amount + OZON_PLUS_SIGN_Y_OFFSET
            draw.text((plus_x, plus_y), "+", font=plus_font, fill=OZON_PLUS_SIGN_COLOR)

        # Отправляем изображение с водяным знаком, если пользователь не авторизован
        send_image_as_file(message.chat.id, img, watermark=not is_user_allowed(message.from_user.id))

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


# Обработка данных для Альфа Банка
def process_alpha_data(message):
    try:
        data = [line.strip() for line in message.text.split('\n') if line.strip()]

        if len(data) != 6:
            bot.send_message(message.chat.id,
                             "Неверный формат данных. Пожалуйста, отправьте 6 строк (3 ФИО и 3 суммы).")
            return

        template = ALPHA_TEMPLATE

        try:
            img = Image.open(template)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Шаблон не найден. Обратитесь к администратору.")
            return

        draw = ImageDraw.Draw(img)

        # Загружаем шрифты
        try:
            name_font = ImageFont.truetype(ALPHA_NAME_FONT_PATH, ALPHA_NAME_FONT_SIZE)
        except:
            name_font = ImageFont.load_default()

        try:
            amount_font = ImageFont.truetype(ALPHA_AMOUNT_FONT_PATH, ALPHA_AMOUNT_FONT_SIZE)
        except:
            amount_font = ImageFont.load_default()

        try:
            plus_font = ImageFont.truetype(ALPHA_PLUS_SIGN_FONT_PATH, ALPHA_PLUS_SIGN_FONT_SIZE)
        except:
            plus_font = ImageFont.load_default()

        try:
            date_font = ImageFont.truetype(ALPHA_DATE_FONT_PATH, ALPHA_DATE_FONT_SIZE)
        except:
            date_font = ImageFont.load_default()

        # Получаем текущую дату в формате "20 ИЮНЯ" (месяц капсом)
        now = datetime.now()
        day = now.day
        month = ["ЯНВАРЯ", "ФЕВРАЛЯ", "МАРТА", "АПРЕЛЯ", "МАЯ", "ИЮНЯ",
                "ИЮЛЯ", "АВГУСТА", "СЕНТЯБРЯ", "ОКТЯБРЯ", "НОЯБРЯ", "ДЕКАБРЯ"][now.month - 1]
        date_text = f"{day} {month}"

        # Рисуем дату на трех разных позициях
        for pos_x, pos_y in ALPHA_DATE_POSITIONS:
            draw.text((pos_x, pos_y), date_text, font=date_font, fill=ALPHA_DATE_COLOR)

        # Обрабатываем ФИО и суммы
        for i in range(0, 6, 2):
            if i + 1 >= len(data):
                break

            name = data[i]
            amount = format_amount(data[i + 1])
            y = ALPHA_NAME_Y_START + (i // 2) * ALPHA_NAME_Y_STEP

            draw.text((ALPHA_NAME_X, y), name, font=name_font, fill=ALPHA_NAME_COLOR)
            bbox = draw.textbbox((0, 0), amount, font=amount_font)
            amount_width = bbox[2] - bbox[0]

            # Рисуем сумму
            draw.text((ALPHA_AMOUNT_X - amount_width, y),
                      amount, font=amount_font, fill=ALPHA_AMOUNT_COLOR)

            # Рисуем знак "+" отдельно с настройками шрифта и смещения
            plus_x = ALPHA_AMOUNT_X - amount_width - 10 + ALPHA_PLUS_SIGN_X_OFFSET
            plus_y = y + ALPHA_PLUS_SIGN_Y_OFFSET
            draw.text((plus_x, plus_y), "+", font=plus_font, fill=ALPHA_PLUS_SIGN_COLOR)

        # Отправляем изображение с водяным знаком, если пользователь не авторизован
        send_image_as_file(message.chat.id, img, watermark=not is_user_allowed(message.from_user.id))

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


# Добавление пользователя (только для админа)
def add_user(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text)
        ALLOWED_USERS.add(user_id)
        bot.send_message(message.chat.id, f"Пользователь {user_id} добавлен.")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID. ID должен быть числом.")


# Удаление пользователя (только для админа)
def remove_user(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text)
        if user_id in ALLOWED_USERS:
            ALLOWED_USERS.remove(user_id)
            bot.send_message(message.chat.id, f"Пользователь {user_id} удален.")
        else:
            bot.send_message(message.chat.id, "Пользователь не найден в списке.")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID. ID должен быть числом.")


# Форматирование суммы
def format_amount(amount_str):
    # Если строка пустая, возвращаем как есть
    if not amount_str:
        return amount_str

    # Проверяем, есть ли в строке запятая или точка
    if ',' in amount_str or '.' in amount_str:
        # Заменяем запятую на точку для корректного преобразования в float
        amount_str = amount_str.replace(',', '.')
        try:
            # Преобразуем в float и форматируем с 2 знаками после запятой
            amount = float(amount_str)
            # Форматируем с запятой в качестве разделителя дробной части
            formatted = "{:,.2f}".format(amount).replace(",", " ").replace(".", ",")
            # Убираем лишние нули после запятой, если они не нужны
            if formatted.endswith(",00"):
                return formatted[:-3]
            return formatted
        except ValueError:
            return amount_str
    else:
        # Для целых чисел просто убираем пробелы и форматируем
        try:
            cleaned = re.sub(r'[,\s]', '', amount_str)
            amount = int(cleaned)
            # Форматируем с пробелами между тысячами
            return "{:,}".format(amount).replace(",", " ")
        except ValueError:
            return amount_str


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)