#Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
#— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
#— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
#— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
#• Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
#• Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
#• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.
#Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
#Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.


from typing import List
from tools import get_password_hash
from fastapi import FastAPI, HTTPException
from sqlalchemy import select, delete, insert, update
from database import startup, shutdown, db
from schemas import UserInSchema, UserSchema, ProductInSchema, ProductSchema, OrderInSchema, OrderSchema, Status
from models import UserModel, ProductModel, OrderModel
from passlib.context import CryptContext

app = FastAPI(title='Seminar_6, dz')
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/users/", response_model=List[UserSchema])
async def get_all_users() -> List[UserSchema]:
    """Получение списка всех пользователей: GET /users/"""
    query = select(UserModel)
    users = await db.fetch_all(query)
    if users:
        return users
    raise HTTPException(status_code=404, detail="Нет ни одного пользователя")


@app.get('/users/{user_id}', response_model=UserSchema)
async def get_single_user(user_id: int) -> UserSchema:
    """Получение информации о конкретном пользователе: GET /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.post('/users/', response_model=UserSchema)
async def create_user(user: UserInSchema) -> dict:
    """Создание нового пользователя: POST /users/"""
    hashed_password = await get_password_hash(user.password)
    user_dict = user.dict()
    user_dict['password'] = hashed_password
    query = insert(UserModel).values(**user_dict)
    user_id = await db.execute(query, user_dict)
    return {**user_dict, 'id': user_id}


@app.put('/users/{user_id}', response_model=UserSchema)
async def update_user(user_id: int, user: UserInSchema) -> UserSchema:
    """Обновление информации о пользователе: PUT /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        updated_user = user.dict(exclude_unset=True)
        if 'password' in updated_user:
            updated_user['password'] = await get_password_hash(updated_user.pop('password'))
        query = update(UserModel).where(UserModel.id == user_id).values(updated_user)
        await db.execute(query)
        return await db.fetch_one(select(UserModel).where(UserModel.id == user_id))
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.delete("/users/{user_id}")
async def delete_user(user_id: int) -> dict:
    """Удаление пользователя: DELETE /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        query = delete(UserModel).where(UserModel.id == user_id)
        await db.execute(query)
        return {'detail': f'Пользователь {db_user.name} с id={db_user.id} удален'}
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.get("/products/", response_model=List[ProductSchema])
async def get_all_products() -> List[ProductSchema]:
    """Получение списка всех товаров: GET /products/"""
    query = select(ProductModel)
    products = await db.fetch_all(query)
    return products


@app.get("/products/{product_id}", response_model=ProductInSchema)
async def get_single_product(product_id: int) -> ProductInSchema:
    """Получение информации о конкретном товаре: GET /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.id == product_id)
    product = await db.fetch_one(query)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.post("/products/", response_model=ProductSchema)
async def create_new_product(product: ProductInSchema) -> dict:
    """Создание нового товара: POST /products/"""
    query = insert(ProductModel)
    new_product = {"product_name": product.product_name, "description": product.description, "price": product.price, "is_del": product.is_del}
    new_product_id = await db.execute(query, new_product)
    return {**new_product, "id": new_product_id}


@app.put("/products/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int, product: ProductInSchema) -> ProductSchema:
    """Обновление информации о товаре: PUT /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.id == product_id)
    product_ = await db.fetch_one(query)
    if product_:
        updated_product = product.dict(exclude_unset=True)
        query = update(ProductModel).where(ProductModel.id == product_id).values(updated_product)
        await db.execute(query)
        return await db.fetch_one(select(ProductModel).where(ProductModel.id == product_id))
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.delete("/products/{product_id}", response_model=str)
async def delete_product(product_id: int):
    query = select(ProductModel).where(ProductModel.id == product_id)
    product = await db.fetch_one(query)
    if product:
        query = delete(ProductModel).where(ProductModel.id == product_id)
        await db.execute(query)
        return f'Товар {product.product_name} удалён.'
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.get("/orders/", response_model=List[OrderSchema])
async def get_all_orders() -> List[OrderSchema]:
    """Получение списка всех заказов: GET /orders/"""
    query = select(OrderModel)
    orders = await db.fetch_all(query)
    return orders


@app.get("/orders/{order_id}", response_model=OrderInSchema)
async def get_single_order(order_id: int) -> OrderInSchema:
    """Получение информации о конкретном заказе: GET /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    order = await db.fetch_one(query)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Заказ не найден")


@app.post("/orders/", response_model=OrderSchema)
async def create_new_order(order: OrderInSchema) -> dict:
    """Создание нового заказа: POST /orders/"""
    query = insert(OrderModel)
    new_order = {"user_id": order.user_id, "product_id": order.product_id, "order_date": order.order_date, "status": order.status}
    new_order_id = await db.execute(query, new_order)
    return {**new_order, "id": new_order_id}


@app.put("/orders/{order_id}", response_model=OrderSchema)
async def update_order(order_id: int, order: OrderInSchema) -> OrderSchema:
    """Обновление информации о заказе: PUT /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    order_ = await db.fetch_one(query)
    if order_:
        updated_order = order.dict(exclude_unset=True)
        query = update(OrderModel).where(OrderModel.id == order_id).values(updated_order)
        await db.execute(query)
        return await db.fetch_one(select(OrderModel).where(OrderModel.id == order_id))
    raise HTTPException(status_code=404, detail="Заказ не найден")


@app.delete("/orders/{order_id}", response_model=str)
async def delete_order(order_id: int):
    query = select(OrderModel).where(OrderModel.id == order_id)
    order = await db.fetch_one(query)
    if order:
        query = delete(OrderModel).where(OrderModel.id == order_id)
        await db.execute(query)
        return f'Заказ {order_id} удален.'
    raise HTTPException(status_code=404, detail="Заказ не найден")

if __name__ == '__main__':
    import asyncio

    asyncio.run(startup())


    async def virgin_db():
        query = delete(UserModel)
        await db.execute(query)
        query = insert(UserModel)
        for i in range(10):
            password = pwd_context.hash(f'password{i}')
            new_user = {"name": f"name{i}", "surname": f"surname{i}", "email": f"user{i}@mail.ru", "password": password}
            await db.execute(query, new_user)


    asyncio.run(virgin_db())