import os
DB_URL = os.getenv("DATABASE_URL")

import psycopg2 as dbapi2

from models.meals import update_stock

def get_all_orders():
  orders = []
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select * from orders"
      cursor.execute(query)
      desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
      for i in cursor:
        res = dict(zip(desc, list(i) ))
        orders.append( res )
  return orders

def get_order(key, type):
  orders = []
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = ""
      if type == "restaurant":
        query = "select * from orders where restaurant_id = %s order by end_at desc;"
      elif type == "user":
        query = "select * from orders where user_id = %s order by end_at desc;"
      else:
        query = "select * from orders where order_id = %s order by end_at desc;"
      cursor.execute(query, (key, ))
      desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
      for i in cursor:
        res = dict(zip(desc, list(i) ))
        orders.append( res )
  return orders

def get_detailed_order_food(key, type):
  orders = []
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = ""
      if type == "restaurant":
        query = "select food_name, brand_name, amount, f.price as price from orders as o full join order_food as of on of.order_id = o.order_id full join food as f on of.food_id = f.food_id where restaurant_id = %s order by end_at desc;"
      elif type == "user":
        query = "select food_name, brand_name, amount, f.price as price from orders as o full join order_food as of on of.order_id = o.order_id full join food as f on of.food_id = f.food_id where user_id = %s order by end_at desc;"
      else:
        query = "select food_name, brand_name, amount, f.price as price from orders as o full join order_food as of on of.order_id = o.order_id full join food as f on of.food_id = f.food_id where o.order_id = %s order by end_at desc;"
      
      cursor.execute(query, (key, ))
      desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
      for i in cursor:
        res = dict(zip(desc, list(i) ))
        orders.append( res )
  return orders

def get_order_details(order_key):
  res = None
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select note, price, o.type as payment_type, created_at, end_at, manager, CONCAT(p.name, ' ', p.surname) as person_name from orders as o full join restaurant as r on o.restaurant_id = r.restaurant_id full join useraccount as u on u.id = o.user_id full join person as p on p.id = u.person where order_id = %s;"
      cursor.execute(query, (order_key, ))
      data = cursor.fetchone()
      if data:
        card = list( data )
        desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
        res = dict(zip(desc, card ))
  return res

def get_order_related_comments(key):
  orders = []
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select title, description, case speed when 0 then 'Slow' else 'Fast' end as speed, case taste when 0 then 'Not tasteful' else 'Tasteful' end as taste, CONCAT(p.name, ' ', p.surname) as person_name from comment as c full join useraccount as u on u.id = c.user_id full join person as p on p.id = u.person where order_id = %s;"
      cursor.execute(query, (key, ))
      desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
      for i in cursor:
        res = dict(zip(desc, list(i) ))
        orders.append( res )
  return orders

def add_order(order):
  order_id = -1
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "insert into orders(price, note, type, rate, end_at, created_at, restaurant_id, user_id) values(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING order_id;"
      cursor.execute(query, order)
      connection.commit()
      order_id = cursor.fetchone()[0]
  return order_id

def connect_order_and_food(orderfood):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "insert into order_food(order_id, food_id, amount) values(%s, %s, %s);"
      cursor.execute(query, orderfood)
      connection.commit()

def make_comment_to_order(comment):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "insert into comment(title, description, speed, taste, user_id, order_id) values(%s, %s, %s, %s, %s, %s);"
      cursor.execute(query, comment)
      connection.commit()

def update_order(order):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "update orders set price = %s, note = %s, type = %s, rate = %s, end_at = %s where order_id = %s;"
      cursor.execute(query, order)
      connection.commit()

def update_order_delivered(order_id):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "update orders set is_delivered = 1 where order_id = %s;"
      cursor.execute(query, (order_id, ))
      connection.commit()

def update_stock_by_order_key(order_id):
  food_list = []
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select food_id, amount from order_food where order_id = %s;"
      cursor.execute(query, (order_id, ))
      for id, amount in cursor:
        for i in range(amount):
          update_stock(id)

def delete_order(order_key):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "delete from orders where order_id = %s;"
      cursor.execute( query, (order_key,) )
      connection.commit()

