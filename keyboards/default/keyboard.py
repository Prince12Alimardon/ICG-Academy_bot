from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Biz haqimizda"),
            KeyboardButton("Kurslar"),
            KeyboardButton("Tezkor aloqa")
        ]
    ],
    resize_keyboard=True
)

phone_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Phone", request_contact=True)
        ]
    ],
    resize_keyboard=True
)


def courses(res: list):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in res:
        markup.insert(KeyboardButton(f"{i['title']}"))

    markup.insert(KeyboardButton("⬅️Ortga"))
    return markup
