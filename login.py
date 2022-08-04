import tkinter as tk
from tkinter import tix
import os
from sqlitedatabase3 import *
from main import *



def get_db_list():
    files = []
    os.getcwd()
    for file in os.listdir(
            os.path.join(os.getcwd())
                            ):
        if '.db' in file :
            files.append(file[:-3])
    return files

print(get_db_list())
def check_password(username,password):
    #  length should be bigger than 6
    #  contains at least one digit but it can't be all digits
    #  string should not contain word "password" and the username in any case
    #  consist of 3 different letters

    check1 = len(password) > 6
    check2 = any([x.isdigit() for x in password]) and not password.isdigit()
    check3 = 'password' not in password and username not in password
    check4 = len(set(password))>=3

    return check1 and check2 and check3 and check4

def check_username(username):

    # username has at least 1 character
    # username doesn't have whitespaces, dots, commas / and \
    # this username isn't already being used

    check1 = len(username) >= 1

    list = [' ','/','.',',','\\']
    check2 = all([x not in username for x in list])

    username_not_duplicated = username not in get_db_list()

    return (check1 and check2 and username_not_duplicated, username_not_duplicated)


def register():
    global username
    global password

    if check_password(username.get(),password.get()) and check_username(username.get()):
        games_table.create_table(username.get())
        user_list.data_entry(username.get(),password.get())
        user_list.get_data()
        messagebox.showinfo('Nice', 'User Successfully Created' )

    else:
        if not check_password(username.get(),password.get()):
            print('niepoprawne chaslo')
        if not check_username(username.get())[1]:
            print('uzytkownik z taka nazwa juz istnieje')
        elif not check_username(username.get())[0]:
            print('niepoprawna nazwa uzytkownika')

def login(window):
    global username
    global password

    check1 = username.get() in get_db_list()
    for element in user_list.get_data():  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! VERY SLOW AND INEFFICIENT
        if element[0] == username.get():
            database_password = element[1]
    check2 = password.get() == database_password

    if check1 and check2:
        print(user_list.get_data())

        window.destroy() # ignore this error?

        play_game(username.get())
    elif not check1:
        messagebox.showinfo('Oh No!', 'Something\'s not right. This user is not in the database!' )
    elif not check2:
        messagebox.showinfo('Oh No!', 'Wrong Password!')


def main_screen():

    window = tix.Tk()
    window.geometry('500x235')
    window.title('Abandon hope all ye who enter here')
    window.iconbitmap(os.path.join('cry.ico'))

    global username
    username = tk.StringVar()
    global password
    password = tk.StringVar()


    tk.Label(window, text = 'login', bg = '#ADD8E6', width = '300', font = ('Calibri',13)).pack()
    tk.Label(text='').pack()

    tk.Label(window, text = 'username',font = ('Calibri',13)).pack()

    username_entry = tk.Entry(window,textvariable = username)
    username_entry.pack()

    tk.Label(window,text = 'password',font = ('Calibri',13)).pack()

    password_entry = tk.Entry(window,textvariable = password)
    password_entry.pack()

    tk.Button(window, text='login', height = '2', width = '15', command = lambda :login(window)).place(relx = 0.550,rely= 0.75)

    tk.Button(window, text='Register',height = '2', width = '15', command = register ).place(relx = 0.225,rely= 0.75)

    tip = tix.Balloon(window)
    tip.bind_widget(password_entry, balloonmsg = '''        Length should be bigger than 6
        Contains at least one digit but it can't be all digits
        String should not contain word "password" and the username in any case
        Consist of 3 different letters''', )

    tip = tix.Balloon(window)
    tip.bind_widget(username_entry, balloonmsg = '''    Username has at least 1 character
    Username doesn't have whitespaces, dots, commas / and \\
    This username isn't already being used''', )

    window.mainloop()

main_screen()
