import tkinter as tk
import  os
from losowanie import *
from tkinter import messagebox
from tkinter import ttk
from sqlitedatabase3 import *
import time
from api import *
import customtkinter


WIDTH = 550
HEIGHT = 350
ile_poprzednich = 0



class Cell():
    all = []

    with open('user.txt') as f:
        username = f.read()
        f.close()
    your_numbers = set()
    your_bonus = None
    game_over = False
    wylosowane = None
    bonus = None
    bonus_true = False
    how_many_guessed = 0
    ile_liczb = 0
    game = None
    game_no = 0
    total_ticket_cost = 0
    total_prize = 0
    try:
        balance = games_table.get_data(username)[-1][-1]
    except:
        balance = 0


    def __init__(self):
        self.is_clicked = False
        self.button_object = None
        self.number = None


    def make_button(self, frame, count_label,balance_label, number=None):
        width = 52
        heigth = 25

        button = customtkinter.CTkButton(master = frame,
                                         text=str(number),
                                         width=width,
                                         height=heigth,
                                         command= lambda: self.left_click(frame, count_label,balance_label),
                                         fg_color=None,
                                         corner_radius=10,
                                         border_width=1)

        self.button_object = button
        self.number = number
        Cell.all.append(self)

    def left_click(self,frame,count_label,balance_label):
        if Cell.game == 'Lotto':
            Cell.ile_liczb = 6
        elif Cell.game == 'EuroMillion':
            Cell.ile_liczb = 6


        how_many_left = Cell.ile_liczb - len(Cell.your_numbers)

        if len(Cell.your_numbers)< Cell.ile_liczb:

            if self.number not in Cell.your_numbers:
                count_label.config(text = f'jeszcze {how_many_left}' if how_many_left != 0 else 'Bonus Round!')

            self.button_object.configure(fg_color='pink')
            Cell.your_numbers.add(self.number)

        elif len(Cell.your_numbers) == Cell.ile_liczb:
            Cell.your_bonus = self.number

            count_label.config(
               text = 'I co wygrałeś?')

            self.button_object.configure(fg_color='blue')
            Cell.wypisz_zwycieskie_cell(frame,count_label,balance_label)

    @staticmethod
    def wypisz_zwycieskie_cell(frame,count_label,balance_label):
        bonus, wylosowane = losowanie(Cell.game)
        for instance in Cell.all:
            if instance.number in wylosowane:
                instance.button_object.configure(
                    text='YES!'
                )
            if instance.number == bonus:
                instance.button_object.configure(
                    text='B!'
                )
        Cell.wylosowane = wylosowane
        Cell.bonus = bonus
        Cell.clicker(frame,count_label,balance_label)

    @staticmethod
    def get_bonus_and_guessed( ):
        Cell.bonus_true = Cell.your_bonus == Cell.bonus
        Cell.how_many_guessed = len([x for x in Cell.your_numbers if x in Cell.wylosowane])

    @staticmethod
    def clicker(frame,count_label,balance_label):

        Cell.get_bonus_and_guessed()
        msg = messagebox.askyesno('wygrałeś?', f'zgadłeś {Cell.how_many_guessed} a bonus {Cell.bonus_true} grasz dalej?')

        if msg == True:
            Cell.show_balance(balance_label)
            Cell.reset_all()
            Cell.start_game(frame,Cell.game, count_label,balance_label)
        else:
            root.destroy()


    @staticmethod
    def show_balance(balance_label):

        if Cell.game == 'Lotto':
            BILET_COST = -2
        if Cell.game == 'EuroMillion':
            BILET_COST = -2.5

        prize = Cell.prize()
        Cell.balance += BILET_COST + prize
        Cell.game_no +=1
        Cell.total_prize += prize
        Cell.total_ticket_cost += BILET_COST

        balance_label.configure(text=f"Your Balance is {Cell.balance} \n"
                                     f" you've played {Cell.game_no} games \n "
                                     f"you've spent {Cell.total_ticket_cost} on tickets \n "
                                     f"you've won {Cell.total_prize} total")


        yournum1, yournum2, yournum3, yournum4, yournum5, yournum6 = Cell.your_numbers
        yourbonus = Cell.your_bonus
        num1, num2, num3, num4, num5, num6= Cell.wylosowane
        bonus = Cell.bonus
        game= Cell.game
        print(Cell.username)
        games_table.data_entry(yournum1, yournum2, yournum3, yournum4, yournum5, yournum6, yourbonus,
                   num1, num2, num3, num4, num5, num6, bonus,game, Cell.balance, Cell.username)



    @staticmethod
    def prize():
        if Cell.game == 'Lotto':
            if Cell.bonus_true:
                prize_list = [0, 0, 3,20,150,100000,2000000]

            else:
                prize_list = [0,0,0,9,50,1500,2000000]
        elif Cell.game == 'EuroMillion':
            if Cell.bonus_true:
                prize_list = [0,0,0,10,100,10000,1000000]
            else:
                prize_list = [0,0,0,3,25,500,10000]


        prize = prize_list[Cell.how_many_guessed]
        return prize

    @staticmethod
    def reset_all():

        Cell.your_numbers = set()
        Cell.bonus = None


        for instance in Cell.all:
            instance.button_object.destroy()

        Cell.all = []

    @staticmethod
    def start_game(frame,game, count_label,balance_label):

        if game == 'Lotto':
            lotto(frame,count_label,balance_label)
        if game == 'EuroMillion':
            euro_million(frame,count_label,balance_label)



#useful functions
def lotto(frame, count_label,balance_label):

    Cell.game = 'Lotto'
    Cell.reset_all()
    number = 1
    for row in range(8):
        for column in range(6):

            if number<48:
                c = Cell()
                c.make_button(frame,count_label,balance_label, number)
                c.button_object.grid(row=row, column=column)

            number +=1
    # Cell.set_username_and_balance()



def euro_million(frame, count_label,balance_label):


    Cell.game = 'EuroMillion'
    Cell.reset_all()
    number = 1
    for row in range(7):
        for column in range(6):

            if number<40:
                c = Cell()
                c.make_button(frame, count_label,balance_label, number)
                c.button_object.grid(row=row, column=column)

            number +=1
    # Cell.set_username_and_balance()


def automatic_lottery_draw(entry,frame, count_label, balance_label):
    global ile_poprzednich
    ile_poprzednich = 0
    game = Cell.game
    how_many_draws = 1

    if entry.get().isnumeric():
        if int(entry.get()) <= 10 and int(entry.get()) > 0:
            how_many_draws = int(entry.get())
        elif int(entry.get()) > 10:
            how_many_draws = 10

    for number in range(how_many_draws):
        los = losowanie(Cell.game)
        yourbonus = Cell.your_bonus = los[0]
        yournum1, yournum2, yournum3, yournum4, yournum5, yournum6 = Cell.your_numbers = los[1]
        los = losowanie(Cell.game)
        bonus = Cell.bonus = los[0]
        num1, num2, num3, num4, num5, num6 = Cell.wylosowane = los[1]

        Cell.get_bonus_and_guessed()
        Cell.show_balance(balance_label)

    pokaz_poprzednie(frame, count_label,balance_label)


def pokaz_poprzednie(frame, count_label,balance_label):
    global ile_poprzednich

    if ile_poprzednich < 10:
        Cell.reset_all()
        (yournum1, yournum2, yournum3, yournum4, yournum5, yournum6, yourbonus,
        num1, num2, num3, num4, num5, num6, bonus, game, balance ) = games_table.get_data(Cell.username)[ile_poprzednich]

        Cell.start_game(frame,game, count_label,balance_label)

        Cell.your_numbers= [yournum1, yournum2, yournum3, yournum4, yournum5, yournum6]
        Cell.your_bonus= yourbonus

        Cell.wylosowane = [num1, num2, num3, num4, num5, num6]
        Cell.bonus = bonus


        count_label.config(text=f'{ile_poprzednich + 1} gra wcześniej')

        for instance in Cell.all:
            if instance.number in Cell.wylosowane:
                instance.button_object.configure(
                    text='YES!'
                )
            if instance.number == Cell.bonus:
                instance.button_object.configure(
                    text='B!'
                )
            if instance.number in Cell.your_numbers:
                instance.button_object.configure(
                    fg_color='pink'
                )
            if instance.number == Cell.your_bonus:
                instance.button_object.configure(
                    fg_color='blue'
                )

        ile_poprzednich +=1
    else:
        ile_poprzednich = 0
        pokaz_poprzednie(frame,count_label,balance_label)

def insert_username(username):
    with open('user.txt','w') as f:
        f.write(username)
        f.close()
        pass

def zeruj_ile_poprzednich():
    global ile_poprzednich
    ile_poprzednich = 0

def get_api(frame, count_label, balance_label):
    results = get_irish_lotto()
    if isinstance(results,list):

        Cell.reset_all()
        numbers = [int(x) for x in results[:-1]]
        bonus = int(results[-1])

        number = 1
        for row in range(8):
            for column in range(6):

                if number < 48:
                    c = Cell()
                    c.make_button(frame, count_label, balance_label, number)
                    c.button_object.grid(row=row, column=column)

                number += 1
        print([instance.number for instance in Cell.all])
        print(numbers)
        print(bonus)

        count_label.configure(text='Would you get this? \n Latest results')

        for instance in Cell.all:
            if instance.number in numbers:
                print('a')
                instance.button_object.configure(
                    text='YES!', fg_color = 'pink'
                )
            if instance.number == bonus:
                instance.button_object.configure(
                    text='B!', fg_color = 'blue'
                )

    else:
        messagebox.showinfo('Error',results)


def play_game(username):

    insert_username(username) # I dont know how to pass username to class so it through a .txt file

    customtkinter.set_appearance_mode('light')
    customtkinter.set_default_color_theme('blue')

    root = customtkinter.CTk()
    root.title('Lotto')
    root.geometry(f'{WIDTH}x{HEIGHT}')
    root.resizable(False,False)
    root.iconbitmap(os.path.join('cry.ico'))

    frame_label = customtkinter.CTkFrame(root, fg_color='#ADD8E6')
    frame_label.place(width = 687, height = 60, x = 0, y = 0) # why width is 687? dunno. It just works

    count_label = tk.Label(master = frame_label,
                           text="Welcome!",
                           bg='#ADD8E6',
                           font="Verdana 15 bold")
    count_label.pack(side=tk.TOP)

    frame = customtkinter.CTkFrame(root, fg_color = 'white')
    frame.place(relx=0.05,rely=0.18)

    try:
        Cell.balance = games_table.get_data(username)[-1][-1]
    except:
        Cell.balance = 1

    frame_balance = customtkinter.CTkFrame(root, fg_color='#ADD8E6')
    frame_balance.place(width = 687, # why width is 687? dunno. It just works
                        height = 90,
                        x = 0,
                        y = HEIGHT-74) # why height = 74? dunno. It just works

    balance_label = tk.Label(master = frame_balance,
                             text=f"Your balance is {Cell.balance}",
                             bg="#ADD8E6",
                             font="Verdana 10 bold")
    balance_label.pack(side=tk.BOTTOM)

    radiovariable = tk.IntVar(value=0)
    radiobutton_1 = customtkinter.CTkRadioButton(master= root,
                                                 text='Lotto',
                                                 variable= radiovariable,
                                                 command= lambda: [lotto(frame,count_label,balance_label), zeruj_ile_poprzednich()],
                                                 value = 0)

    radiobutton_2 = customtkinter.CTkRadioButton(master = root,
                                                 text="Euro Million",
                                                 variable= radiovariable,
                                                 command= lambda: [euro_million(frame,count_label,balance_label), zeruj_ile_poprzednich()],
                                                 value = 1)

    radiobutton_1.place(relx = 0.65, rely=0.18)
    radiobutton_2.place(relx=0.8, rely=0.18)

    entry = customtkinter.CTkEntry(master = root,
                                   width = 130,
                                   corner_radius=10,
                                   border_width=3,
                                   placeholder_text= 'How many games?',
                                   placeholder_text_color='grey')
    entry.place(relx=0.65,rely=0.28)

    button = customtkinter.CTkButton(master = root,
                                     text= 'Wybierz \n automatycznie',
                                     width=130,
                                     height= int(HEIGHT/500),
                                     command = lambda: automatic_lottery_draw(entry,frame, count_label,balance_label),
                                     corner_radius=10, border_width=1)

    button.place(relx=0.65,rely=0.38)

    button = customtkinter.CTkButton(master = root,
                                     text= 'Pokaż \n poprzednie',
                                     width=130,
                                     height= int(HEIGHT/500),
                                     command = lambda: pokaz_poprzednie(frame,count_label,balance_label),
                                     corner_radius=10,
                                     border_width=1 )
    button.place(relx=0.65,rely=0.51)

    button =  customtkinter.CTkButton(master = root,
                                      text= 'get api',
                                      width=130,
                                      height= int(HEIGHT/500),
                                      command = lambda: get_api(frame, count_label, balance_label),
                                      corner_radius=10,
                                      border_width=1)
    button.place(relx=0.65,rely=0.64)

    lotto(frame,count_label,balance_label)

    #mainloop
    root.mainloop()

# if __name__ == '__main__':
#      play_game('Lottery')