import random
from support import *
from cell import *


def lotto(frame):

    Cell.game = 'Lotto'


    Cell.reset_all()
    number = 1
    for row in range(8):
        for column in range(6):

            if number < 48:
                c = Cell()
                c.make_button(frame, number)
                c.button_object.grid(row=row, column=column)

            number += 1


def euro_million(frame):
    Cell.game = 'EuroMillion'
    Cell.reset_all()
    number = 1
    for row in range(7):
        for column in range(6):

            if number < 40:
                c = Cell()
                c.make_button(frame, number)
                c.button_object.grid(row=row, column=column)

            number += 1

