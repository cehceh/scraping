import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


domain =  "https://ar.wikipedia.org"

url = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"


def scraping_wikipedia():

    response = requests.get(url)

    soup = bs(response.content, features='html.parser')

    table = soup.select('table.wikitable')[0]

    columns = [i.get_text(strip=True) for i in table.find_all("th")] 

    columns += ["رابط الكتاب", "رابط المؤلف", "رابط البلد"]

    data = []

    for tr in table.find("tbody").find_all("tr"):
        cells = []
        link=[]
        tds = tr.find_all('td')

        for td in tds:
            cells.append(td.get_text(strip=True))
            if td.find('a'):
                link.append(domain + td.find('a')['href']) 
        data.append(cells + link)


    df = pd.DataFrame(data, columns=columns)

    df.to_excel("data.xlsx", index=False)

    return df



scraping_wikipedia()

