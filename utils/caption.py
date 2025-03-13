from database.db_utils import db_get_Finally_cart_products



def text_or_caption(name, description, price):
    text = f'<b>{name}</b>\n\n'
    text+= f'<b>Інгрідієнти: </b>{description}\n'
    text+=f'💸 Ціна : {price} гр.'
    return text


def matem_product_in_carts(chat_id, user_text):
    product = db_get_Finally_cart_products(chat_id)
    if product:
        text = f'<b>{user_text}</b>\n\n'
        total_products = total_price = count = 0
        for name, quantity, price, cart_id in product:
            count +=1
            total_products +=1
            total_price += price
            
            text +=f'\n{count} {name}\nКількість {quantity}\nВартість: {price} Гр.\n\n '
        text +=f'\nКатегорій товарів у кошику: {total_products}\nЗагальна вартість кошику:\n💸💸💸        {total_price}Гр.       💸💸💸\n'
        
        context = (count, text, total_price, cart_id)
        return context