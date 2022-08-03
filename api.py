import requests as r
from bs4 import BeautifulSoup
import re

def get_polish_lotto():
    response = r.get(
        'http://serwis.mobilotto.pl/mapi_v6/index.php?json=getGames')

    wylosowane = (response.json()['Lotto']['numerki'])\
                    .split(',')

    return wylosowane


def get_irish_lotto():
    try:
        URL = 'https://www.rte.ie/lotto/'
        page = r.get(URL)

        soup = BeautifulSoup(page.content, features="html.parser")

        page = soup.find_all('span')
        numbers = []

        for sth in page:
            text = sth.get_text()

            if text.isnumeric():
                numbers.append(text)
            if len(numbers) == 7:
                 break

        return numbers
    except r.exceptions.ConnectionError as e:
        return e