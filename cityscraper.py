import re
import os
from requests import get
from bs4 import BeautifulSoup

url = 'http://www.city-data.com/neighborhood/Roslindale-Roslindale-MA.html'

response = get(url)
soup = BeautifulSoup(response.text, 'html.parser')

citystats = soup.find_all('div', class_ = 'content-item')

def no_blanks(text):
    return os.linesep.join([s for s in text.splitlines() if s])

def scrape_div(index):
    try:
        my_set = citystats[index].find_all('div', class_ = 'hgraph')
        if len(my_set) > 0:
            for more in my_set:
                return no_blanks(more.get_text())
        else:
            return no_blanks(citystats[index].get_text())
    except:
        return "No data."

area_pop = scrape_div(0)
income = scrape_div(1)
rent = scrape_div(2)
housing = scrape_div(15)
