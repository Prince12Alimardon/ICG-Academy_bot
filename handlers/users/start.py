from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.keyboard import courses, buttons, phone_button
from loader import dp
import requests
from data.config import IP
from states.state import CourseDescription, Phone
from aiogram.dispatcher import FSMContext
from keyboards.inline.keyboard import register


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    requests.post(url=f"{IP}/telegram-users/", data={'telegram_id': message.from_user.id})
    await message.answer(f"Assalomu-alaykum, {message.from_user.full_name}!", reply_markup=buttons)


@dp.message_handler(text='Kurslar')
async def course(message: types.Message):
    qs = requests.get(url=f"{IP}/courses/")
    await CourseDescription.description.set()
    await message.answer('O\'zingizga kerakli kursni tanlang👇', reply_markup=courses(qs.json()))


@dp.message_handler(state=CourseDescription.description)
async def about_course(message: types.Message, state: FSMContext):
    if message.text == "⬅️Ortga":
        await message.answer("Siz bosh menuga qaytdingiz", reply_markup=buttons)
        await state.finish()
    qs = requests.post(url=f"{IP}/courses/?title={message.text}")
    ab = qs.json()
    await message.answer_photo(open(ab['image_path'], 'rb'), caption=f"{ab['description']}", reply_markup=register)
    await state.finish()


@dp.callback_query_handler(text='register')
async def reqister(message: types.CallbackQuery):
    await Phone.phone.set()
    await message.message.answer('Telefon raqamingizni kiriting yoki Phone tugmasini tanlang: ', reply_markup=phone_button)


@dp.message_handler(state=Phone.phone, content_types='contact')
async def sdsfd(message: types.Message, state: FSMContext):
    if message.contact:
        qs = requests.post(url=f"{IP}/user-create/",
                           data={'telegram_id': message.from_user.id, 'name': message.from_user.full_name,
                                 'phone': message.contact.phone_number})
    else:
        qs = requests.post(url=f"{IP}/user-create/",
                           data={'telegram_id': message.from_user.id, 'name': message.from_user.full_name,
                                 'phone': message.text})

    await state.finish()
    await message.answer('Biz siz bilan tez orada aloqaga chiqamiz', reply_markup=buttons)


@dp.message_handler(text='Biz haqimizda')
async def about(message: types.Message):
    qs = requests.get(url=f"{IP}/about/")
    ab = qs.json()
    await message.answer_photo(open(ab['image'], 'rb'), caption=f"{ab['description']}", reply_markup=buttons)


@dp.message_handler(text='Tezkor aloqa')
async def phone(message: types.Message):
    qs = requests.get(url=f"{IP}/about/")
    ab = qs.json()
    await message.answer(f"Yordam uchun: {ab['phone']}", reply_markup=buttons)


@dp.message_handler(text='⬅️Ortga')
async def phone(message: types.Message):
    await message.answer("Siz bosh menuga qaytdingiz", reply_markup=buttons)
