from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, Session
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, DECIMAL, BigInteger, ForeignKey, DateTime , func
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

BD_USER = os.getenv("DB_USER")
BD_PASSWORD = os.getenv("DB_PASSWORD")
BD_ADRESS = os.getenv("DB_ADRESS")
BD_NAME = os.getenv("DB_NAME")


engine = create_engine(f'postgresql://{BD_USER}:{BD_PASSWORD}@{BD_ADRESS}', echo=False)

class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    update: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Users(Base):
    __tablename__='users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=True)
    
    carts: Mapped[int] = relationship('Carts', back_populates='user_cart')
    
    def __str__(self):
        return self.name
    
class Carts(Base):
    __tablename__='carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[int] = mapped_column(DECIMAL(12, 2), default=0)
    total_products: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    
    user_cart: Mapped[Users] = relationship(back_populates='carts')
    finally_id: Mapped[int] = relationship('Finally_carts', back_populates='user_cart')
   
    
    def __str__(self):
        return str(self.id)

class Finally_carts(Base):
    __tablename__='finally_carts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    finally_price:Mapped[DECIMAL] = mapped_column(DECIMAL(12 ,2))
    quantity:Mapped[int] 
    
    
    cart_id:Mapped[int] = mapped_column(ForeignKey('carts.id'))
    user_cart: Mapped['Carts'] = relationship(back_populates='finally_id')
    
    
    def __str__(self):
        return str(self.id)
  
  

class Historys(Base):
    __tablename__='historys'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]  
    telegram_id:Mapped[int] = mapped_column((BigInteger))
    def __str__(self):
        return str(self.id)
  
  
  
  
  
  
  
  
  
  
  
  
    
class Categories(Base):
    
    __tablename__='categories'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    category_name:Mapped[str] = mapped_column(String(20), unique=True)
    
    products = relationship('Products', back_populates='product_category')
    
    
    def __str__(self):
        return self.category_name


class Products(Base):
    __tablename__='products'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    product_name:Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str]
    image:Mapped[str] = mapped_column(String(160))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(20, 2))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    
    product_category:Mapped[Categories] = relationship(back_populates='products')
    
    
class Akcii(Base):
    __tablename__='akcii'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(30))
    descriptions:Mapped[str] = mapped_column(String(150))  
    images:Mapped[str] = mapped_column(String(160))  
    
    

   
   
   
   
   
   
   
   
    
    
    
    
    
def main():
   Base.metadata.drop_all(engine)
   
   Base.metadata.create_all(engine)

   categories = ("Чипси М'ясні", "Ковбаски", "Ковбаси", "Масики" )
  
   with Session(engine) as session:
       for category in categories:
            query = Categories(category_name=category)
            session.add(query)
            session.commit()
        
       
            
            
if __name__ == '__main__':
    main()