from enum import Enum
import datetime
from pydantic import EmailStr, BaseModel, Field


class Status(Enum):
    """Перечисление статусов заказов"""
    DONE = 'Выполнен'
    IN_PROGRESS = 'На выполнении'


class UserInSchema(BaseModel):
    """Модель пользователя без id"""
    name: str = Field(..., min_length=2, title='Задается имя пользователя')
    surname: str = Field(..., min_length=2, title='Задается фамилия пользователя')
    email: EmailStr = Field(..., min_length=5, title='Задается email пользователя')
    password: str = Field(..., max_length=25, min_length=3, title='Задается пароль пользователя')

class UserSchema(UserInSchema):
    """Модель пользователя с id"""
    id: int


class ProductInSchema(BaseModel):
    """Модель товара без id"""
    product_name: str = Field(..., min_length=3, title='Задается название товара')
    description: str = Field(default=None, min_length=3, title='Описание товара (не обязательно)')
    price: float = Field(..., max_length=15, title='Задается цена товара')
    
class ProductSchema(ProductInSchema):
    """Модель товара с id"""
    id: int


class OrderInSchema(BaseModel):
    """Модель заказа без id"""
    order_date = datetime.date = Field(..., title='Задается дата выполнения заказа')
    status: Status = Status.IN_PROGRESS

class OrderSchema(OrderInSchema):
    """Модель заказа с id"""
    id: int