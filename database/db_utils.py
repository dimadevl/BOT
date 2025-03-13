from typing import Iterable
from sqlalchemy.orm import Session , joinedload
from sqlalchemy import delete, update, select, Subquery
from database.models import Carts, Categories, Finally_carts, Products, Users,Akcii,Historys, engine
from sqlalchemy.sql.functions import sum
from sqlalchemy import DECIMAL





with Session(engine) as session:
    db_session = session
     
    
    
def db_register_user(full_name: str, chat_id:int) -> bool:
    """Первая регистрация пользователя"""
    try:
        query = Users(name=full_name, telegram=chat_id)
        db_session.add(query)
        db_session.commit()
        return False
    except:
        db_session.rollback()
        return True
    
    
    
    
    
def db_update_users(chat_id:int, full_name: str, phone):
    """Поделиться контактом"""
    try:
        query = Users(telegram = chat_id,
                      name=full_name,
                      phone=phone)
        db_session.add(query)
        db_session.commit()
    except:
        db_session.rollback()
        query = update(Users).where(Users.telegram == chat_id).values(name = full_name,
                                                                      phone=phone)
        db_session.execute(query)
        db_session.commit()
    
    
def db_create_user_cart(chat_id: int):
    """Создание временной корзинки пользователя"""
    try:
        subquery = db_session.scalar(select(Users).where(Users.telegram == chat_id))
        query = Carts(user_id = subquery.id)
        db_session.add(query)
        db_session.commit()
        return True
    except AttributeError:
        """Если отправил контакт анонимній пользователь"""
        db_session.rollback()
    except:
        """Если карта существует"""
        db_session.rollback()
   
def db_get_category() -> Iterable:
    """Получаес все категории"""
    query = select(Categories)
    return db_session.scalars(query)       

def db_get_products(category_id):
    query = select(Products).where(Products.category_id == category_id)
    return db_session.scalars(query)
    
def  db_product_by_id(product_id:int) ->Products:
    query = select(Products).where(Products.id == product_id) 
    return db_session.scalar(query)   




def db_get_user_cart(chat_id: int) -> Carts:
    query = select(Carts).join(Users).where(Users.telegram == chat_id)
    return db_session.scalar(query)
    
def db_update_carts(price: DECIMAL, cart_id: int, quantity=1) ->None:
    query = update(Carts).where(Carts.id == cart_id).values(total_price=price,
                                                            total_products=quantity)
    db_session.execute(query)
    db_session.commit()





def db_inser_or_update_finally_cart(cart_id, product_name, total_products, total_price):
    """Вносим новые данные либо редактируем"""
    try:
        query = Finally_carts(cart_id=cart_id, 
                              product_name=product_name,
                              quantity=total_products,
                              finally_price=total_price)
        db_session.add(query)
        db_session.commit()
        return True
    except:
        db_session.rollback()
        query = update(Finally_carts).where(Finally_carts.product_name == product_name
                                            ).where(Finally_carts.cart_id == cart_id
                                                    ).values(quantity=total_products,
                                                             finally_price=total_price)
        db_session.execute(query)
        db_session.commit()
        return False
    
def db_get_product_by_name(product_name:str):
    """Получаем продут по имени"""
    query = select(Products).where(Products.product_name == product_name)
    return db_session.scalar(query)


def db_get_finally_price(chat_id: InterruptedError):
    query = select(sum(Finally_carts.finally_price)).join(Carts).join(Users).where(Users.telegram == chat_id)
    return db_session.execute(query).fetchone()[0]
    
def db_get_Finally_cart_products(chat_id:int)->Iterable:
    """Получаем список товаров по телеграм айди пользователя"""
    
    query = select(Finally_carts.product_name,
                   Finally_carts.quantity,
                   Finally_carts.finally_price,
                   Finally_carts.cart_id).join(Carts).join(Users).where(Users.telegram == chat_id)
    return db_session.execute(query).fetchall()
    
def db_delate_product(chat_id: int):
    query = select(Finally_carts.id,
                   Finally_carts.product_name).join(Carts).join(Users).where(Users.telegram == chat_id)
    return db_session.execute(query).fetchall()
    
    
    
def db_product_delate_by_id(finally_id:int) ->None:
    query = delete(Finally_carts).where(Finally_carts.id == finally_id)
    db_session.execute(query)
    db_session.commit()
    
def db_get_user_info(chat_id: int):
    query = select(Users).where(Users.telegram == chat_id)
    return db_session.scalar(query)

def db_get_akcii():
    query = select(Akcii)
    return db_session.scalars(query)

def db_delete_akcii(akcii_id):
    query = delete(Akcii).where(Akcii.id == akcii_id)
    db_session.execute(query)
    db_session.commit()
 

 
def db_get_final(chat_id):
    query = select(Finally_carts.product_name,
                   Finally_carts.quantity,
                   Finally_carts.finally_price).join(Carts).join(Users).where(Users.telegram == chat_id)
    return db_session.scalars(query)
 
 
 
 
 
 
 
 
    
    
def db_update_history(text, telegram_id):
    
    try:
        query = Historys(text=text, telegram_id=telegram_id)
        db_session.add(query)
        db_session.commit()
        return False
    except:
        db_session.rollback()
        query = update(Historys).where(telegram_id=telegram_id,
                                       text=text)
        db_session.execute(query)
        db_session.commit()
        return True

def db_clear_finally_cart(cart_id:int) ->None:
    query = delete(Finally_carts).where(Finally_carts.cart_id == cart_id)
    db_session.execute(query)
    db_session.commit()
    
def db_get_historys(chat_id:int):
    query = select(Historys).where(Historys.telegram_id == chat_id)
    return db_session.scalars(query)

def db_get_assorti():
    query = select(Products)
    return db_session.scalars(query)

def db_delete_assorti(product_id):
    query = delete(Products).where(Products.id == product_id)
    db_session.execute(query)
    db_session.commit()