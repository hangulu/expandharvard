import re
import os
from requests import get
from bs4 import BeautifulSoup

def formatter(text):
    no_lines = os.linesep.join([s for s in text.splitlines() if s])
    x = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", no_lines)
    for i in range(len(x)):
        try:
            x[i] = int(x[i].replace(',', ''))
        except:
            x[i] = float(x[i].replace(',', ''))
    return x

def scrape_div(citystats, index):
    try:
        my_set = citystats[index].find_all('div', class_ = 'hgraph')
        if len(my_set) > 0:
            for more in my_set:
                return formatter(more.get_text())
        else:
            return formatter(citystats[index].get_text())
    except:
        return "No data."

def scraper(city, ctype, endpoint):
    url = 'http://www.city-data.com/{}/{}.html'.format(ctype.lower(), endpoint)
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    labels = ['City', 'Area', 'Population Density', 'City Income', 'City Rent', 'City Housing Price']

    if ctype == 'Neighborhood':
        citystats = soup.find_all('div', class_ = 'content-item')
        area_pop = scrape_div(citystats, 0)
        income = scrape_div(citystats, 1)
        rent = scrape_div(citystats, 2)
        housing = scrape_div(citystats, 15)

        if (rent == 'No data.'):
            r = rent
        else:
            r = int(rent[1])
        values = [city, area_pop[0], area_pop[2], income[0], r, housing[0]]
    elif ctype == 'City':
        raw_pop_dense = soup.find_all('section', class_ = 'population-density')
        raw_income = soup.find_all('section', class_ = 'median-income')
        raw_rent = soup.find_all('section', class_ = 'median-rent')
        area_pop = scrape_div(raw_pop_dense, 0)
        income = scrape_div(raw_income, 0)
        rent = scrape_div(raw_rent, 0)
        housing = scrape_div(raw_income[0].find_all('div', class_ = 'hgraph'), 1)

        if (rent == 'No data.'):
            r = rent
        else:
            r = int(rent[1])
        values = [city, area_pop[0], area_pop[1], income[0], r, housing[0]]
    else:
        return "No"

    return dict(zip(labels, values))
