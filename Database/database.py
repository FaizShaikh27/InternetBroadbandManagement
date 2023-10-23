import sqlite3

def create_tables():
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            payment_done REAL NOT NULL,
            internet_plan TEXT NOT NULL,
            duration_of_plan INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

def add_admin(username, password, phone_number):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO admins (username, password, phone_number) VALUES (?, ?, ?)', (username, password, phone_number))
    connection.commit()
    connection.close()

def get_all_clients():
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    connection.close()
    return clients


def add_client(username, password, full_name, address, phone_number, internet_plan, duration_of_plan, payment_done):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO clients (username, password, full_name, address, phone_number, payment_done, internet_plan, duration_of_plan) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (username, password, full_name, address, phone_number, payment_done, internet_plan, duration_of_plan))
    connection.commit()
    connection.close()




def get_client_by_username(username):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM clients WHERE username = ?', (username,))
    client = cursor.fetchone()
    connection.close()
    return client


def update_client(client_data):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    username = client_data["username"]

    cursor.execute('''
        UPDATE clients
        SET username = ?,
            password = ?,
            full_name = ?,
            address = ?,
            phone_number = ?,
            payment_done = ?,
            internet_plan = ?,
            duration_of_plan = ?
        WHERE username = ?
    ''', (
        username,
        client_data["password"],
        client_data["full_name"], 
        client_data["address"],
        client_data["phone_number"],
        client_data["payment_done"],
        client_data["internet_plan"],
        client_data["duration"],
        username
    ))
    
    connection.commit()
    connection.close()





def get_client_data(username):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('SELECT username, password, internet_plan, duration_of_plan FROM clients WHERE username = ?', (username,))
    client_data = cursor.fetchone()
    connection.close()

    if client_data:
        data_dict = {
            "username": client_data[0],
            "password": client_data[1],
            "internet_plan": client_data[2],
            "duration": client_data[3]
        }
        return data_dict
    else:
        return None 




def update_payment_done(username, payment_done):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE clients SET payment_done = ? WHERE username = ?', (payment_done, username))
    connection.commit()
    connection.close()


def update_internet_plan_duration(username, internet_plan, duration):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE clients SET internet_plan = ?, duration_of_plan = ? WHERE username = ?', (internet_plan, duration, username))
    connection.commit()
    connection.close()


def get_client_by_phone_number(phone_number):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM clients WHERE phone_number = ?', (phone_number,))
    client_data = cursor.fetchone()
    connection.close()

    if client_data:
        client_dict = {
            "id": client_data[0],
            "username": client_data[1],
            "password": client_data[2],
            "full_name": client_data[3],
            "address": client_data[4],
            "phone_number": client_data[5],
            "payment_done": client_data[6],
            "internet_plan": client_data[7],
            "duration_of_plan": client_data[8]
        }
        return client_dict
    else:
        return None 


def update_password(username, new_password):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE clients SET password = ? WHERE username = ?', (new_password, username))
    connection.commit()
    connection.close()


def update_internet_plan_duration(username, internet_plan, duration):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE clients SET internet_plan = ?, duration_of_plan = ? WHERE username = ?', (internet_plan, duration, username))
    connection.commit()
    connection.close()

def get_client_password(username):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('SELECT password FROM clients WHERE username = ?', (username,))
    password = cursor.fetchone()
    connection.close()

    if password:
        return password[0]
    else:
        return None  