from aiogram.utils.keyboard import  InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.db_utils import db_get_category, db_get_products, db_get_finally_price, db_delate_product, db_get_akcii, db_get_assorti


def generator_category_manu(chat_id:int):
    categories = db_get_category()
    total_price = db_get_finally_price(chat_id)
    keyboard = InlineKeyboardBuilder()
    
    
    keyboard.button(text=f'Ваш кошик 🛒: {total_price if total_price else 0 } Гр.', callback_data='Ваша корзинка')
    for category in categories:
        keyboard.button(text=category.category_name , callback_data=f'category_{category.id}') 
        keyboard.adjust(1, 2)
    return keyboard.as_markup(resize_keyboard=True)

def product_by_categoria(category_id:int) -> InlineKeyboardMarkup:
    
    products =db_get_products (category_id)
    
    keyboard = InlineKeyboardBuilder()
    
    [keyboard.button(text=product.product_name, callback_data=f'product_{product.id}') for product in products]
    keyboard.adjust(2)
        
    keyboard.row(InlineKeyboardButton(text='Назад ◀️', callback_data='return_to_categor'))
    
    return keyboard.as_markup()
    
def constructor_plus_minus(quantity=1) ->InlineKeyboardMarkup:
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text='➖', callback_data='action -')
    keyboard.button(text=str(quantity), callback_data='quantity')
    keyboard.button(text='➕', callback_data='action +')
    keyboard.button(text='😛 Покласти у кошик 😛', callback_data='put_ipnto_cart_')
    keyboard.adjust(3, 1)
    
    
    return keyboard.as_markup()


def generate_delete_product(chat_id: int):
    keyboard = InlineKeyboardBuilder()
    
    carts_product = db_delate_product(chat_id)
    
    keyboard.button(text='Оформити замовлення 🖋️', callback_data='order')
    for finally_cart_id, product_name in carts_product:
        keyboard.button(text=f'del❌{product_name}', callback_data=f'delete_{finally_cart_id}')
        keyboard.adjust(1)
    return keyboard.as_markup()

def menu_cart_reply(chat_id):
    total_price = db_get_finally_price(chat_id)
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text=f'Ваш кошик 🛒: {total_price if total_price else 0} Гр.', callback_data='Ваша корзинка')
    return keyboard.as_markup()

def delete_batton_akcii():
    akcii = db_get_akcii()
    
    
    keyboard = InlineKeyboardBuilder()
    
    for prod in akcii:
        if prod:
            keyboard.button(text ='Удалить акцию', callback_data=f'deletes_{prod.id}')
            
    return keyboard.as_markup()


def assorti_product(product_id):
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text='Удалить товар', callback_data=f'delassorti_{product_id}')
    return keyboard.as_markup()
