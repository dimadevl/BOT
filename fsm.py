from aiogram import Router, types, Bot, Dispatcher, F
from aiogram.filters import Command
from keyboards.reply import generator_keyboard_reply, fsm_catalog
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db_utils import db_session, db_get_akcii, db_delete_akcii
from database.models import Akcii, Categories, Products
from keyboards.inline import delete_batton_akcii
from database.db_utils import db_update_users, db_create_user_cart




admin_router = Router()




class AddProduct(StatesGroup):
    name = State()
    descriptions = State()
    images = State()

class AddTovar(StatesGroup):
    category_id = State()
    product_name= State()
    price = State()
    description = State()
    image = State()



ADMIN_KB = generator_keyboard_reply(
    'Каталог',
    'Добавить товар акции',
    'Текущая акция',
    'Вернуться к старту',
     placeholder='Выберите действие',
     sizes=(2, 1, 2)
)

CATALOG_KB = fsm_catalog()


@admin_router.message(Command('YUL', prefix='@'))
async def comanda_admina(message:types.Message):
    await message.answer('Что вы хотите сделать', reply_markup=ADMIN_KB)





    
@admin_router.message(StateFilter(None),F.text == 'Добавить товар акции')
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Введите название акции", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)
    
@admin_router.message(StateFilter('*'), Command('Отмена'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def back_state(message:types.Message, state:FSMContext):
    curent_state = state.get_state()
    if curent_state is None:
        return
    await state.clear()
    await message.answer('Действия отменены', reply_markup=CATALOG_KB)
    
    
    
    
@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажите описание акции")
    await state.set_state(AddProduct.descriptions)
    
@admin_router.message(AddProduct.descriptions, F.text)
async def add_descrip(message: types.Message, state: FSMContext):
    await state.update_data(descriptions=message.text)
    await message.answer("Завантажте фото")
    await state.set_state(AddProduct.images)
    
@admin_router.message(AddProduct.images, F.photo)
async def add_image(message: types.Message, state:FSMContext):
    await state.update_data(images=message.photo[-1].file_id)
    await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    db_session.add(Akcii(
        name = data["name"],
        descriptions = data["descriptions"],
        images = data["images"],))
    
    db_session.commit()
    await state.clear()
    
@admin_router.message(F.text == 'Текущая акция')
async def delete_tovar_in_akcii(message:types.Message, bot:Bot):
    chat_id = message.chat.id
    prod = db_get_akcii()
    for i in prod:
        text = f'{i.name}, {i.descriptions}'
        await bot.send_photo(chat_id=chat_id, photo=i.images, caption=text, reply_markup=delete_batton_akcii())
        
@admin_router.callback_query(F.data.contains('deletes_'))
async def delate_akcion(callback:types.CallbackQuery, bot:Bot):
    chat_id = callback.from_user.id
    akcii_id = callback.data.split('_')[-1]
    db_delete_akcii(akcii_id)
    await bot.send_message(chat_id=chat_id, text='Акция удаленна')
    await callback.answer()

@admin_router.message(F.text == 'Каталог')
async def catalog_get(message:types.Message, bot:Bot):
    chat_id = message.chat.id
    await bot.send_message(chat_id = chat_id, text='Вы перешли в раздел редактирования товаров каталога', reply_markup=CATALOG_KB)
    
    
@admin_router.message(StateFilter(None), F.text == 'Добавить продукт🥩')
async def add_product_catalog(message:types.Message, state:FSMContext):
    await message.answer("Введите категорию продукта по номеру 1.Чипси М'ясні, 2.Ковбаски, 3.Ковбаси, 4.Масики", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddTovar.category_id)
    
@admin_router.message(AddTovar.category_id, F.text)
async def add_categori_id(message:types.Message, state:FSMContext):
    try:
        float(message.text)
        await state.update_data(category_id = message.text)
    except ValueError:
        await message.answer('Введите цифры')
        return
    await state.update_data(category_id = message.text)
    await message.answer('Теперь напишите имя продукта')
    await state.set_state(AddTovar.product_name)

@admin_router.message(AddTovar.product_name, F.text)
async def add_name_catalog(message:types.Message, state:FSMContext):
    await state.update_data(product_name= message.text)
    await message.answer('Теперь укажите цену этого продукта')
    await state.set_state(AddTovar.price)
    
@admin_router.message(AddTovar.price, F.text)
async def add_price_catalog(message:types.Message, state:FSMContext):
    try:
        float(message.text)
        await state.update_data(price=message.text)
    except ValueError:
        await message.answer('Вы ввели не коректное значение')
        return    
    
    await state.update_data(price=message.text)
    await message.answer('Теперь опишите продукт')
    await state.set_state(AddTovar.description)
    
@admin_router.message(AddTovar.description, F.text)
async def add_descr_catalog(message:types.Message, state:FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Добавьте фото')
    await state.set_state(AddTovar.image)
    
@admin_router.message(AddTovar.image, F.photo)
async def add_image_catalog(message:types.Message, state:FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer('Товар добавлен', reply_markup=ADMIN_KB)
    data = await state.get_data()
    db_session.add(Products(category_id=data["category_id"],
                            product_name= data ["product_name"],
                            price = data ["price"],
                            description = data ["description"],
                            image = data["image"]))
    db_session.commit()
    await state.clear()

@admin_router.message(F.text == 'Назад ⏪')
async def back_admin(message:types.Message):
    await comanda_admina(message)
    
