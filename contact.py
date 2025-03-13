from aiogram import Bot, Router,types, F
from database.db_utils import db_update_users, db_create_user_cart
from aiogram.types import Message
from keyboards.reply import kb_menu
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


contact_router = Router()






async def menu_proces(message:Message):
    await message.answer(text='Здійсніть вибір', reply_markup=kb_menu())






@contact_router.message((F.contact) | (F.text))
async def update_contact( message:types.Message, state:FSMContext):
    if message.text == None:
        chat_id = message.chat.id
        phone = message.contact.phone_number
        full_name = message.from_user.full_name 
        db_update_users(chat_id, phone , full_name)
    else:
        await message.answer('Не коректні данні - натисніть кнопку')
        return
    if db_create_user_cart(chat_id=chat_id):
            await message.answer('Регістрація пройшла успішно')
    await menu_proces(message)
   