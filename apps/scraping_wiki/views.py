from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import requests
import pygsheets


def create_excel(request):

    file_path = os.path.join(settings.BASE_DIR, "sheets/data.xlsx")

    domain = 'https://ar.wikipedia.org'

    url = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"

    response = requests.get(url)

    soup = bs(response.content, features='html.parser')

    table = soup.select('table.wikitable')[0]

    columns = [i.get_text(strip=True) for i in table.find_all("th")]

    columns += ["رابط الكتاب", "رابط المؤلف", "رابط البلد"]

    data = []

    for tr in table.find("tbody").find_all("tr"):
        cells = []
        tds = tr.find_all('td')
        link = []

        for td in tds:
            cells.append(td.get_text(strip=True))
            if td.find('a'):
                link.append(domain + td.find('a')['href'])
        data.append(cells + link)

    df = pd.DataFrame(data, columns=columns)

    df.to_excel(file_path, index=False)

    return HttpResponse("Data Has Been Written Successfully")


def create_google_sheet(request):

    domain = 'https://ar.wikipedia.org'

    url = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"

    response = requests.get(url)

    soup = bs(response.content, features='html.parser')

    table = soup.select('table.wikitable')[0]

    columns = [i.get_text(strip=True) for i in table.find_all("th")]

    columns += ["رابط الكتاب", "رابط المؤلف", "رابط البلد"]

    data = []

    for tr in table.find("tbody").find_all("tr"):
        cells = []
        tds = tr.find_all('td')
        link = []

        for td in tds:
            cells.append(td.get_text(strip=True))
            if td.find('a'):
                link.append(domain + td.find('a')['href'])
        data.append(cells + link)

    df = pd.DataFrame(data, columns=columns)

    gc = pygsheets.authorize(
        service_file=os.path.join(
            settings.BASE_DIR, "best-100-novel-a99af0da7cee.json"
        )
    )
    
    sheet = gc.open('test')
    work_book = sheet[0]
    work_book.set_dataframe(df, start=(1, 1))

    return HttpResponse("Data Has Been Written Successfully")