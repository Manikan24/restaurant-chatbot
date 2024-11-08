import sqlite3
import json

def create_db():
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    price REAL,
                    availability INTEGER,
                    category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )''')
    conn.commit()
    conn.close()

def store_menu_in_db(menu_data):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()

    for category in menu_data['menu']:
        category_name = category['category']
        c.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
        category_id = c.lastrowid
        
        for item in category['items']:
            c.execute('''INSERT INTO items (name, description, price, availability, category_id) 
                         VALUES (?, ?, ?, ?, ?)''', 
                         (item['name'], item['description'], item['price'], item['availability'], category_id))
    
    conn.commit()
    conn.close()

def get_menu_from_db():
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute('''SELECT categories.name, items.id, items.name, items.description, items.price, items.availability 
                 FROM items INNER JOIN categories ON items.category_id = categories.id''')
    menu = c.fetchall()
    conn.close()
    return menu

def get_categories_from_db():
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute("SELECT * FROM categories")
    categories = c.fetchall()
    conn.close()
    return categories

def update_item_in_db(item_id, name, description, price, availability, category_id):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute('''UPDATE items SET name = ?, description = ?, price = ?, availability = ?, category_id = ?
                 WHERE id = ?''', (name, description, price, availability, category_id, item_id))
    conn.commit()
    conn.close()

def delete_item_from_db(item_id):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute('''DELETE FROM items WHERE id = ?''', (item_id,))
    conn.commit()
    conn.close()

def add_item_to_db(name, description, price, availability, category_id):
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute('''INSERT INTO items (name, description, price, availability, category_id) 
                 VALUES (?, ?, ?, ?, ?)''', (name, description, price, availability, category_id))
    conn.commit()
    conn.close()
