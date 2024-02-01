from sqlalchemy import Column, Integer, String, Enum, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from schemas import Status

Base = declarative_base()


class UserModel(Base):
    """Таблица Users"""
    __tablename__ = 'Users'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(length=50), unique=True, index=True)
    surname = Column(String(length=50), unique=True, index=True)
    email = Column(String(length=50), unique=True, index=True)
    password = Column(String, nullable=False)

    def __str__(self):
        return self.name, self.surname

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, surname={self.surname}, email={self.email})'

class ProductModel(Base):
    """Таблица Products"""
    __tablename__ = 'Products'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    product_name = Column(String(length=50), unique=True, index=True)
    description = Column(String(length=250), index=True)
    price = Column(float(length=15), index=True)
    is_del = Column(Boolean, nullable=False)
    
    def __str__(self):
        return self.product_name

    def __repr__(self):
        return f'Product(id={self.id}, product_name={self.product_name}, price={self.price}, status={self.status})'

class OrderModel(Base):
    """Таблица Orders"""
    __tablename__ = 'Orders d пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, foreign_key=True, nullable=False)
    product_id = Column(Integer, foreign_key=True, nullable=False)
    order_date = Column(Date)
    status = Column(Enum(Status), nullable=False)
    
    def __str__(self):
        return self.id

    def __repr__(self):
        return f'Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, order_date={self.order_date}, status={self.status})'