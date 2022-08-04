import sqlite3
import os

class games_table():

    @staticmethod
    def create_table(username):
        conn = sqlite3.connect(os.path.join(os.getcwd(), str(username) + '.db'))
        c = conn.cursor()
        try:
            c.execute('CREATE TABLE games(yournum1 INTEGER,yournum2 INTEGER,yournum3 INTEGER,yournum4 INTEGER,'
                  'yournum5 INTEGER,yournum6 INTEGER,yourbonus7 INTEGER, num1 INTEGER,num2 INTEGER,num3 INTEGER,'
                  'num4 INTEGER,num5 INTEGER,num6 INTEGER,bonus INTEGER,game TEXT, balance REAL)')
        except sqlite3.OperationalError as e:
            print(e)
        conn.commit()
        c.close()
        conn.close()

    @staticmethod
    def data_entry(yournum1,yournum2,yournum3,yournum4,yournum5,yournum6,yourbonus,
                   num1,num2,num3,num4,num5,num6,bonus,game,balance,username):
        conn = sqlite3.connect(os.path.join(os.getcwd(), str(username) + '.db'))
        c = conn.cursor()
        c.execute('INSERT INTO games VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                  (yournum1,yournum2,yournum3,yournum4,yournum5,yournum6,yourbonus,
                   num1,num2,num3,num4,num5,num6,bonus,game,balance))
        conn.commit()
        c.close()
        conn.close()

    @staticmethod
    def get_data(username):
        conn = sqlite3.connect(os.path.join(os.getcwd(), str(username) + '.db'))
        c = conn.cursor()
        c.execute('SELECT * FROM games ORDER BY rowid DESC LIMIT 10;')
        data = c.fetchall()
        c.close()
        conn.close()
        return data


class user_list():
    @staticmethod
    def create_table():
        conn = sqlite3.connect(os.path.join(os.getcwd(), 'users' + '.db'))
        c = conn.cursor()
        try:
            c.execute('CREATE TABLE IF NOT EXISTS users(user TEXT, password TEXT)')
        except sqlite3.OperationalError:
            pass
        c.close()
        conn.close()

    @staticmethod
    def data_entry(user,password):
        conn = sqlite3.connect(os.path.join(os.getcwd(), 'users' + '.db'))
        c = conn.cursor()
        c.execute('INSERT INTO users VALUES(?,?)',
                  (user,password))
        conn.commit()
        c.close()
        conn.close()

    @staticmethod  # under construction
    def get_data():
        conn = sqlite3.connect(os.path.join(os.getcwd(), 'users' + '.db'))
        c = conn.cursor()
        c.execute('SELECT * FROM users ORDER BY rowid DESC LIMIT 10;') #
        data = c.fetchall()
        c.close()
        conn.close()
        return data
