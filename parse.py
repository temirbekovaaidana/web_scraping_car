import requests
from bs4 import BeautifulSoup
import csv

URL = "https://cars.kg/offers"
HEADERS = {
    "users-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "accept": "*/*",
}
LINK = "https://cars.kg"
CSV_FILE = "cars.csv"

def get_html(url, headers):
    response = requests.get(url, headers=headers)
    return response

def get_content_from_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    items = soup.find_all("a", class_="catalog-list-item")
    cars = []
    for item in items:
        cars.append(
            {
                "title": item.find("span", class_="catalog-item-caption").get_text().replace("\n", ""),
                "description": item.find("span", class_="catalog-item-descr").get_text().replace("\n",""),
                "km": item.find("span",class_="catalog-item-mileage").get_text().replace("\n",""),
                "price": item.find("span", class_="catalog-item-price").get_text().replace("\n", ""),
                "image": LINK + item.find("img").get("src"),

            }
        )
    return cars

def save_data(cars: list) -> None:
    with open(CSV_FILE, "w") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["Название", "Описание", "Пробег", "Цена", "Картинка"])
        for car in cars:
            writer.writerow([car["title"],car["description"],car["km"],car["price"], car["image"]])

def get_result_parse():
    html = get_html(URL, HEADERS)
    if html.status_code == 200:
        cars = get_content_from_html(html.text)
        save_data(cars)
        return cars

print(get_result_parse())