import sqlite3

conn = sqlite3.connect('cafe.db')
cur=conn.cursor()

cur.execute("")
conn.commit()
row=cur.fetchall()
print(row)

# print("DB success")
# conn.execute('CREATE TABLE IF NOT EXISTS customer (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,phone INTEGER,email TEXT,password TEXT,status INTEGER,flag INTEGER)')
# print("CUSTOMER created")
# conn.execute('CREATE TABLE IF NOT EXISTS product(p_id INTEGER PRIMARY KEY AUTOINCREMENT,p_name TEXT,p_price INTEGER)')
# print("PRODUCT created")
# conn.execute('CREATE TABLE IF NOT EXISTS order_items(order_id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,product_id INTEGER,no_items INTEGER,total_price REAL,flag INTEGER,FOREIGN KEY (user_id) REFERENCES customer(id),FOREIGN KEY (product_id) REFERENCES product(p_id))')
# print("ORDER_ITEM created")
# conn.execute('CREATE TABLE IF NOT EXISTS dealer(d_id INTEGER PRIMARY KEY AUTOINCREMENT,d_name TEXT,d_oid INTEGER,d_flag INTEGER,FOREIGN KEY (d_oid) REFERENCES order_items(order_id))')
# print("DEALER created")

# conn.execute('CREATE TABLE IF NOT EXISTS orders (o_id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,FOREIGN KEY (user_id) REFERENCES customer(id))')
# print("ORDER created")

cur.close()