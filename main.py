import asyncio
import html
import os
from aiogram import Bot, Dispatcher, types, F

from os import getenv

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())





from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.reply import *
from keyboards.inline import *
from database.db_utils import *
from aiogram.types import CallbackQuery , FSInputFile, InputMediaPhoto
from utils.caption import *
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.formatting import  as_marked_section, Bold , as_list
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime ,timedelta
from utils.apsched import akcii, text_and
from utils import apsched
from utils.caption import matem_product_in_carts
from aiogram.enums import ParseMode
from fsm import admin_router
from contact import contact_router
from contact import menu_proces
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(os.getenv('TOKEN') , default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
MANAGER=os.getenv("MANAGER")











@dp.message(CommandStart())
async def command_start(message:Message):
    await message.answer(f'<b>!! Ми ради вас бачити 😎 {message.from_user.full_name} !!</b>\n 😃 <b>!!!</b>Вас вітає бот з доставки Dikiy_Kaban<b>!!!</b> 😃\n            <b>🍺🍺🍺Снеків🍺🍺🍺</b>\n                <b>🐗Дикий кабан🐗</b>')
    await register_user(message)
    
async def register_user(message:Message):
    """Первичная авторизация запись имя и телеграм айди в базу"""
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    if db_register_user(full_name, chat_id):
        await message.answer('Авторизація пройшла успішно')
        
        await menu_proces(message)
    else:
        await bot.send_message(chat_id=chat_id, text='У нас не має вашого номера🤫', reply_markup=share_phone_batton())
    










        

        
        # TODO        


@dp.message(F.text == '🐗 Зробити замовлення 🐗')
async def order_by(message: types.Message):
    """Отправка меню"""
    chat_id = message.chat.id
    
    await bot.send_message(chat_id=chat_id, text='поїхали', reply_markup=back_to_manu())
    await bot.send_message(chat_id=chat_id, text='Оберіть категорію', reply_markup=generator_category_manu(chat_id))

@dp.message(F.text.regexp(r'^Г[а-я]+ [а-я]{4}'))
async def return_to_main_manu(message:types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id -1)
    
    await menu_proces(message)
    
    
@dp.callback_query(F.data.regexp(r'category_[1-9]'))
async def shov_product_batton(callback:CallbackQuery):
    """Показ категорий"""
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    category_id = int(callback.data.split('_')[-1])
    await bot.edit_message_text(text='Оберіть продукт', chat_id=chat_id, message_id=message_id, reply_markup=product_by_categoria(category_id))
    

@dp.callback_query(F.data.contains('product_'))
async def shov_product_detale(callback:CallbackQuery):
    """Показ продукта"""
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    product_id = int(callback.data.split('_')[-1])
    product = db_product_by_id(product_id)
    await bot.delete_message(chat_id=chat_id, 
                             message_id=message_id)
    if user_cart := db_get_user_cart(chat_id):
        
        db_update_carts(price=product.price, cart_id=user_cart.id)
        
        text = text_or_caption(product.product_name, product.description, product.price)
        
        
        await bot.send_message(chat_id=chat_id, text='Зробіть вибір модефікатору', reply_markup=back_batton())
        await bot.send_photo(chat_id=chat_id, photo=product.image, caption=text, reply_markup=constructor_plus_minus())
        
    else:
        await bot.send_message(chat_id=chat_id, text = 'Немає вашого контакту', reply_markup=share_phone_batton() )
        
        
        
          
          
          
          


@dp.message(F.text == 'Назад◀️')
async def return_to_product_menu(message: Message):
    await bot.delete_message(message.chat.id, message.message_id-1)
    
    await order_by(message)
        


@dp.callback_query(F.data == 'return_to_categor')
async def return_tocategory_batton(callback:CallbackQuery):
    """Кнопка назад"""
    chat_id = callback.from_user.id
    message_id = callback.message.message_id
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Зробіть вибір', reply_markup=generator_category_manu(chat_id))

@dp.callback_query(F.data.regexp(r'action [+-]'))
async def constructor_change(callback: CallbackQuery):
    """Обработка колбека плюс и минус во времнной корзине"""
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    action = callback.data.split()[-1]
    product_name = callback.message.caption.split('\n')[0]
    product = db_get_product_by_name(product_name)
    product_price = product.price
    user_cart = db_get_user_cart(chat_id)
    if action == '+':
            user_cart.total_products +=1
            product_price = product_price*user_cart.total_products
            db_update_carts(price=product_price, quantity=user_cart.total_products,
                            cart_id=user_cart.id) 
    if action == '-':   
            if user_cart.total_products < 2:
                await callback.answer('Меньше одного товару не можна', show_alert=True)
            else:    
                user_cart.total_products -=1
                product_price = product_price*user_cart.total_products
                db_update_carts(price=product_price, quantity=user_cart.total_products,
                            cart_id=user_cart.id) 
            
    text = text_or_caption(product.product_name, 
                           product.description, 
                           product_price)
    image = InputMediaPhoto(media=product.image, caption=text)
    
    try:
        await bot.edit_message_media(chat_id=chat_id, message_id=message_id, 
                                     media=image, reply_markup=constructor_plus_minus(user_cart.total_products))
    except TelegramBadRequest:
        pass
       
 
            
            
    
@dp.callback_query(F.data == 'put_ipnto_cart_')
async def put_into_cart(callback: CallbackQuery):
    """Реакция на нажатие на кнопку положить в корзинку"""
    chat_id = callback.from_user.id
    product_name = callback.message.caption.split('\n')[0]
    cart = db_get_user_cart(chat_id)
    
    
    await bot.delete_message(chat_id=chat_id, message_id=callback.message.message_id)
    
    if db_inser_or_update_finally_cart(cart_id=cart.id, product_name=product_name, total_products=cart.total_products, total_price=cart.total_price):
        await bot.send_message(chat_id=chat_id, text='Продукт добавлен❤️')
    else:
        await bot.send_message(chat_id=chat_id, text='Кількість змінена✍️')
        
        
        
    await order_by(callback.message)



@dp.callback_query(F.data == 'Ваша корзинка')
async def shov_finally_cart(callback: CallbackQuery):
    message_id = callback.message.message_id
    chat_id = callback.from_user.id
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    context = matem_product_in_carts(chat_id, user_text='💲💲💲💲   Ваш кошик   💲💲💲💲')
    if context:
        count, text, *_ = context
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=generate_delete_product(chat_id))
    else:
        await bot.send_message(chat_id=chat_id, text='Кошик пустий ☹️')
        await order_by(callback.message)


@dp.callback_query(F.data.contains('delete_'))
async def order_manager(callback: CallbackQuery):
    finally_id = callback.data.split('_')[-1]
    db_product_delate_by_id(finally_id=finally_id)
    await bot.answer_callback_query(callback_query_id=callback.id, text='Продукт видален', show_alert=True)
    
    await shov_finally_cart(callback)






@dp.callback_query(F.data.contains('order'))
async def order_manager(callback:CallbackQuery):
    chat_id = callback.from_user.id
    message_id = callback.message.message_id
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    caunt, text, total_price, cart_id = context = matem_product_in_carts(chat_id, user_text='Замовлення')
    user = db_get_user_info(chat_id=chat_id)
    text += f'Имя заказчика {user.name}\nКонтактный номер {user.phone} '
    
    await bot.send_message(chat_id=MANAGER, text=text )
    await bot.send_message(chat_id=chat_id, text="Дякуємо за замовлення!Очікуйте на зв'язок 📱 з нашим менеджером - ваше замовлення в роботі😎🐗")
    
    telegram_id = callback.from_user.id
    db_update_history(text , telegram_id)
    
    db_clear_finally_cart(cart_id=cart_id)  
    sheduler = AsyncIOScheduler(timezone="Europe/Kiev")
    sheduler.add_job(apsched.text_order, trigger='date', run_date=datetime.now() + timedelta(seconds=5), kwargs={'bot':bot,  'message':callback.message, } )
    sheduler.start()
    
    
    sheduler = AsyncIOScheduler(timezone="Europe/Kiev")
    sheduler.add_job(apsched.akcii, trigger='date', run_date=datetime.now() + timedelta(seconds=10), kwargs={'bot':bot,  'message':callback.message, } )
    sheduler.start()
    
    sheduler = AsyncIOScheduler(timezone="Europe/Kiev")
    sheduler.add_job(apsched.text_and, trigger='date', run_date=datetime.now() + timedelta(seconds=15), kwargs={'bot':bot,  'message':callback.message, } )
    sheduler.start()
    
    
    
    
    


@dp.message(F.text == 'Кошик 🛒')
async def back_to_cart(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text='😃', reply_markup=menu_cart_reply(chat_id=chat_id))
    await bot.send_message(chat_id=chat_id, text='Натисніть на кошик чи натисніть кнопку Головне Меню🥙', reply_markup=back_to_manu())
    

@dp.message(F.text == 'Контакти 📱')
async def info_handler(message: types.Message):
    chat_id = message.chat.id
    text = as_list(as_marked_section(Bold('Контакти:'), 'Менеджер: @Ulia22000', marker='📞'),as_marked_section(Bold('Доставка:'), "Нова пошта 🚒, Кур'єром 🛵"),
                   as_marked_section(Bold('Наш час праці'), '9.00 = 20.00', marker='⏲️'), sep='\n------------------------------------------------\n')
    await bot.send_message(chat_id=chat_id, text =text.as_html())


@dp.message(F.text == 'Акції 🎉')
async def akcii_handler(message: types.Message):
    chat_id = message.chat.id
    akcii = db_get_akcii()
    if akcii:
        for prod in akcii:
            text = as_list(as_marked_section(Bold(f'🎉Назва акції:\n{prod.name}'), f'Опис акції:\n{prod.descriptions}', marker='🎁'), as_marked_section(Bold('✨Наступна акція кожний місяць з початку місяця😃'),'А далі ще цікавіше з\n           🐗ТД.Дикий Кабан🐗', marker='🎈'), sep='\n⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐\n')
            await bot.send_photo(chat_id = chat_id, photo=prod.images, caption=text.as_html(), reply_markup=back_to_manu())
    else:
        await bot.send_message(chat_id=chat_id, text='На днний час акції немає🤫')
        
@dp.message(F.text == 'Історія 📓')
async def history_handler(message:types.Message):
    chat_id= message.from_user.id
    carts = db_get_historys(chat_id)
    if carts:
        for cart in carts:
            text = f'Ваше попереднє замовлення: {cart.created} {cart.text} по вашому айді {cart.telegram_id}'
            await bot.send_message(chat_id=chat_id, text =text)
    else:
        await bot.send_message(chat_id=chat_id, text='Ваша історія пуста')
















@dp.message(F.text == 'Вернуться к старту')
async def start_bot(message:types.Message):
    await command_start(message)

@dp.message(F.text == 'Ассортимент товаров 🅰️')
async def assortiment(message:types.Message):
    chat_id = message.chat.id
    product = db_get_assorti()
    if product:
        for prod in product:
            product_id = prod.id
            text = f'{prod.description}'
            await bot.send_photo(chat_id=chat_id, photo =prod.image, caption=text, reply_markup=assorti_product(product_id))
        


@dp.callback_query(F.data.contains('delassorti_'))
async def delete_assorti(callback:CallbackQuery):
    chat_id = callback.message.chat.id
    product_id = callback.data.split('_')[-1]
    db_delete_assorti(product_id)
    await bot.send_message(chat_id=chat_id, text='Товар удален')
    await callback.answer()



















   
dp.include_router(admin_router)   
dp.include_router(contact_router)
   
   
   
   
   
    
    

async def main():
    
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    asyncio.run(main())