import bs4
from bs4 import BeautifulSoup
from typing import Iterable
import requests
import re


URL_KULINARIJA = "https://ital-kvartal.ru/kulinarija/"
URL_KONDITERSKAJA = "https://ital-kvartal.ru/konditerskaja/"


def get_page(url: str) -> requests.models.Response:
    page = requests.get(url)
    page.encoding = 'utf-8'
    return page


def find_product_cards(page: requests.models.Response) -> bs4.element.ResultSet:
    soup = BeautifulSoup(page.text, "html.parser")
    return soup.find_all("div", class_="w-grid-item-h")


def make_product_list(cards: bs4.element.ResultSet) -> Iterable[str]:
    for item in cards:
        string = re.sub(r"(от\s)", repl=" ", string=item.text)
        string = re.sub(r"[.)].*$", repl="", string=string).strip("\n")
        yield string


def make_product_links(cards: bs4.element.ResultSet) -> Iterable[str]:
    for item in cards:
        try:
            yield item.div.span.a.get('href')
        except AttributeError:
            yield item.a.get('href')


def write_data_to_file(items: Iterable[str], links: Iterable[str], file_name: str) -> None:
    with open(f"{file_name}.txt", 'wt', newline="", encoding="utf-8") as text_in:
        for i, j in zip(items, links):
            if i != " ":
                text_in.write(f'{i}) Ссылка: {j}\n')
            else:
                text_in.write(f'Торт на заказ Ссылка: {j}\n')


def main(url: str, file_name: str) -> None:
    page = get_page(url)
    product_cards = find_product_cards(page)
    product_list = make_product_list(product_cards)
    product_links = make_product_links(product_cards)
    write_data_to_file(product_list, product_links, file_name)


if __name__ == '__main__':
    main(URL_KULINARIJA, "kulinarija")
    main(URL_KONDITERSKAJA, "konditerskaja")
