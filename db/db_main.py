import sqlite3
from db import queries

db = sqlite3.connect('db/db.sqlite3')
cursor = db.cursor()


async def sql_create():
    if db:
        print("База данных SQLite3 подключена!")
    cursor.execute(queries.CREATE_TABLE_REGISTRATION)
    cursor.execute(queries.CREATE_TABLE_PRODUCTS)
    cursor.execute(queries.CREATE_TABLE_PRODUCTS_DETAILS)
    cursor.execute(queries.CREATE_TABLE_COLLECTION_PRODUCTS)
    db.commit()


async def sql_insert_registration(telegram_id, firstname):
    cursor.execute(queries.INSERT_INTO_TABLE_REGISTRATION, (
        telegram_id, firstname
    ))
    db.commit()


async def sql_insert_products(name, size, price, id_product, photo):
    cursor.execute(queries.INSERT_PRODUCTS, (
        name,
        size,
        price,
        id_product,
        photo
    ))
    db.commit()


async def sql_insert_products_details(category, info_product, id_product):
    cursor.execute(queries.INSERT_PRODUCTS_DETAILS, (
        category,
        info_product,
        id_product
    ))
    db.commit()


async def sql_insert_collection_products(product_id, collection):
    print('Колекция')
    cursor.execute(queries.INSERT_COLLECTION_PRODUCTS, (
        product_id,
        collection
    ))
    db.commit()
