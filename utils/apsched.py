
from aiogram import  types, Bot, F

from keyboards.reply import *
from keyboards.inline import *
from database.db_utils import *

from aiogram.utils.formatting import  as_marked_section, Bold , as_list

from utils.apsched import *
from aiogram import Bot






















async def akcii(message: types.Message, bot:Bot):
    chat_id = message.chat.id
    akcii = db_get_akcii()
    for prod in akcii:
        text =as_list(as_marked_section(Bold(f'🎉Назва акції:\n{prod.name}'), f'Опис акції:\n{prod.descriptions}', marker='🎁'), as_marked_section(Bold('✨Наступна акція кожний місяць з початку місяця😃'),'Кожний місяц ще цікавіше з \n           🐗ТД.Дикий Кабан🐗', marker='🎈'), sep='\n⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐\n')
        await bot.send_photo(chat_id = chat_id, photo=prod.images, caption=text.as_html(), reply_markup=back_to_manu())


async def text_order(message: types.Message, bot:Bot):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text='Також перегляньте поки чекаєте на замовлення акцію😄')
    
async def text_and(message:types.Message, bot:Bot):
    chat_id =message.chat.id
    await bot.send_message(chat_id=chat_id, text='Тож смачного вам до нової зустрічи!💋💋💋💋💋💋💋💋💋💋💋💋💋💋')