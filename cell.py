from support import *
import tkinter as tk
import  os
from losowanie import *
from tkinter import messagebox
from tkinter import ttk
from support import *
import time



class Cell(root):

    all = []
    your_numbers = set()
    your_bonus = None
    game_over = False
    wylosowane = None
    bonus = None
    bonus_true = False
    how_many_guessed = 0
    ile_liczb = 0
    balance = 0
    game = None


    #balance_label = tk.Label(root, text=f"Your Balance is {Cell.balance}", fg="black", font="Verdana 15 bold")
    #balance_label.pack(side=tk.BOTTOM)

    balance_label = tk.Label(root, text="Your Balance is", fg="black", font="Verdana 15 bold")
    balance_label.pack(side=tk.BOTTOM)

    def __init__(self):
        self.is_clicked = False
        self.button_object = None
        self.number = None

    def make_button(self, frame, number=None, width = int(WIDTH/85), heigth = int(HEIGHT/500)):
        button = tk.Button(frame, text=str(number), width=width, height=heigth, command= self.left_click)

        #button.bind('<Button-1>', self.left_click)

        self.button_object = button
        self.number = number


        Cell.all.append(self)




    def left_click(self):


        if Cell.game == 'Lotto':
            Cell.ile_liczb = 6
        elif Cell.game == 'EuroMillion':
            Cell.ile_liczb = 6

        how_many_left = Cell.ile_liczb - len(Cell.your_numbers)


        if len(Cell.your_numbers)< Cell.ile_liczb:
            Cell.show_count(f'jeszcze {how_many_left}' if how_many_left != 0 else 'Bonus Round!')
            self.button_object.configure(bg='pink')
            Cell.your_numbers.add(self.number)



        elif len(Cell.your_numbers) == Cell.ile_liczb:
            Cell.your_bonus = self.number
            Cell.show_count('I co wygrałeś?')
            self.button_object.configure(bg='blue')
            Cell.wypisz_zwycieskie_cell()

    @staticmethod
    def wypisz_zwycieskie_cell():
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
        Cell.clicker()

    @staticmethod
    def clicker( ):

        Cell.bonus_true = Cell.your_bonus == Cell.bonus
        Cell.how_many_guessed = len([x for x in Cell.your_numbers if x in Cell.wylosowane])
        msg = messagebox.askyesno('wygrałeś?', f'zgadłeś {Cell.how_many_guessed} a bonus {Cell.bonus_true} grasz dalej?')

        if msg == True:
            Cell.show_balance()
            Cell.reset_all()
            Cell.start_game()
        else:
            root.destroy()

    @staticmethod
    def show_count( text):

        count_label.config(text=text)

    @staticmethod
    def show_balance():

        if Cell.game == 'Lotto':
            BILET_COST = -2
        if Cell.game == 'EuroMillion':
            BILET_COST = -2.5

        Cell.balance += BILET_COST + Cell.prize()
        balance_label.configure(text=f"Your Balance is {Cell.balance}")

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
    def start_game():
        if Cell.game == 'Lotto':
            lotto()
        if Cell.game == 'EuroMillion':
            euro_million()



class Game():


    count_label = tk.Label(root, text="Welcome!", fg="black", font="Verdana 15 bold")
    count_label.pack(side=tk.TOP)

    balance_label = tk.Label(root, text=f"Your Balance is {Cell.balance}", fg="black", font="Verdana 15 bold")
    balance_label.pack(side=tk.BOTTOM)