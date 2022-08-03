import random

def losowanie(game):
    if game == 'Lotto':
        number = 7 # 6 numerów + bonus
        cells = 48
    elif game == 'EuroMillion':
        number = 7 # 6 numerów + bonus
        cells = 40
    allnumbers = [i for i in range(1,cells)]

    a=random.choice(allnumbers)
    victory = []
    for _ in range(number):
        a=random.choice(allnumbers)
        allnumbers.remove(a)
        victory.append(a)
    #bonus = victory[-1]
    #victory = victory[:-1]

    return (victory[-1],victory[:-1])