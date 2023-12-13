from bs4 import BeautifulSoup
import requests
import re

URL_KULINARIJA = "https://ital-kvartal.ru/kulinarija/"
URL_KONDITERSKAJA = "https://ital-kvartal.ru/konditerskaja/"


def get_page(url):
    page = requests.get(url)
    page.encoding = 'utf-8'
    return page


def make_food_list(page):
    soup = BeautifulSoup(page.text, "html.parser")
    page_items = soup.find_all("div", class_="w-grid-item-h")
    print(page_items[0])
    page_links = []
    for item in page_items:
        try:
            page_links.append(item.div.span.a.get('href'))
        except AttributeError:
            page_links.append(item.a.get('href'))
    return page_items, page_links


def format_food_list(items):
    for item in items:
        string = re.sub(r"(от\s)", repl=" ", string=item.text)
        string = re.sub(r"[.)].*$", repl="", string=string).strip("\n")
        yield string


def main(url, file_name):
    page = get_page(url)
    items, links = make_food_list(page)
    formatted_items = format_food_list(items)

    with open(f"{file_name}.txt", 'wt', newline="", encoding="utf-8") as text_in:
        for i, j in zip(formatted_items, links):
            if i != " ":
                text_in.write(f'{i}) Ссылка: {j}\n')
            else:
                text_in.write(f'Торт на заказ Ссылка: {j}\n')


if __name__ == '__main__':
    main(URL_KULINARIJA, "kulinarija")
    main(URL_KONDITERSKAJA, "konditerskaja")
