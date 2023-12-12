from bs4 import BeautifulSoup
import requests
import re

URL = "https://ital-kvartal.ru/kulinarija/"

page = requests.get(URL)
page.encoding = 'utf-8'

soup = BeautifulSoup(page.text, "html.parser")

all_food = soup.find_all("div", class_="w-grid-item-h")
links = [link.div.span.a.get('href') for link in all_food]


def make_food_list(food):
    for position in food:
        string = re.sub(r"(от\s)", repl=" ", string=position.text)
        string = re.sub(r"[.)].*$", repl="", string=string).strip("\n")
        yield string


if __name__ == '__main__':
    result = list(make_food_list(all_food))

    with open("menu.txt", 'wt', newline="", encoding="utf-8") as text_in:
        for i, j in zip(result, links):
            text_in.write(f'{i}) Ссылка: {j}\n')
