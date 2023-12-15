from bs4 import BeautifulSoup
import requests
import re


URL_KULINARIJA = "https://ital-kvartal.ru/kulinarija/"
URL_KONDITERSKAJA = "https://ital-kvartal.ru/konditerskaja/"


def get_page(url):
    page = requests.get(url)
    page.encoding = 'utf-8'
    return page


def find_food_cards(page):
    soup = BeautifulSoup(page.text, "html.parser")
    return soup.find_all("div", class_="w-grid-item-h")


def make_food_list(cards):
    for item in cards:
        string = re.sub(r"(от\s)", repl=" ", string=item.text)
        string = re.sub(r"[.)].*$", repl="", string=string).strip("\n")
        yield string


def make_food_links(cards):
    for item in cards:
        try:
            yield item.div.span.a.get('href')
        except AttributeError:
            yield item.a.get('href')


def write_data_to_file(items, links, file_name):
    with open(f"{file_name}.txt", 'wt', newline="", encoding="utf-8") as text_in:
        for i, j in zip(items, links):
            if i != " ":
                text_in.write(f'{i}) Ссылка: {j}\n')
            else:
                text_in.write(f'Торт на заказ Ссылка: {j}\n')


def main(url, file_name):
    page = get_page(url)
    food_cards = find_food_cards(page)
    food_list = make_food_list(food_cards)
    food_links = make_food_links(food_cards)
    write_data_to_file(food_list, food_links, file_name)


if __name__ == '__main__':
    main(URL_KULINARIJA, "kulinarija")
    main(URL_KONDITERSKAJA, "konditerskaja")
