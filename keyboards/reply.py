from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, BigInteger, DECIMAL, Integer
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from aiogram.utils.keyboard import ReplyKeyboardBuilder 
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


load_dotenv()


def share_phone_batton() -> ReplyKeyboardMarkup:
    
    keyboard = ReplyKeyboardBuilder()
    
    keyboard.button(text='Відправити для вдалої регістрації контакт ☎️', request_contact=True)
    return keyboard.as_markup(resize_keyboard=True)

def kb_menu() -> ReplyKeyboardBuilder:
    
    keyboard = ReplyKeyboardBuilder()
    
    keyboard.button(text='🐗 Зробити замовлення 🐗')
    keyboard.button(text='Контакти 📱')
    keyboard.button(text='Кошик 🛒')
    keyboard.button(text='Акції 🎉')
    keyboard.button(text='Історія 📓')
    keyboard.adjust(1, 3)
    
    return keyboard.as_markup(resize_keboard=True)


def back_to_manu() ->ReplyKeyboardBuilder:
    
    keyboard = ReplyKeyboardBuilder()
    
    keyboard.button(text='Головне меню')
    
    return keyboard.as_markup(resize_keyboard=True)
    
def back_batton() ->ReplyKeyboardMarkup:
    
    keyboard = ReplyKeyboardBuilder()
    
    keyboard.button(text='Назад◀️')
    
    return keyboard.as_markup(resize_keyboard=True)

def fsm_catalog():
    
    keyboard = ReplyKeyboardBuilder()
    
    keyboard.button(text='Добавить продукт🥩')
    keyboard.button(text='Ассортимент товаров 🅰️')
    keyboard.button(text='Назад ⏪')
    keyboard.adjust(2,1)
    
    return keyboard.as_markup(resize_keyboard=True)










def generator_keyboard_reply(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2, 1),
):
    
    keyboard = ReplyKeyboardBuilder()
    
    for index, text in enumerate(btns, start=0):
        
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        
        else:
            keyboard.add(KeyboardButton(text=text))
            
    return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)       