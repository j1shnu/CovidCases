#!/usr/bin/env python
# (c) Jishnu
import requests, sys
from bs4 import BeautifulSoup as soup

# World wide status
def world():
    uClient = requests.get("https://www.worldometers.info/coronavirus/")
    src = uClient.content
    uClient.close()

    page = soup(src, 'html.parser')
    containers = page.findAll("div", {"class": "content-inner"})

    # Gathering Details
    container1 = containers[0].findAll("div", {"id": "maincounter-wrap"})
    caseLabel = container1[0].h1.text
    caseNumbers = container1[0].span.text.strip()

    deathLabel = container1[1].h1.text
    deathNumbers = container1[1].span.text.strip()

    recoverLabel = container1[2].h1.text
    recoverNumber = container1[2].span.text.strip()

    print("\nCORONA(COVID-19) WORLD WIDE CASES\n{6}\n{0}  {1}\n{2}  {3}\n{4}  {5}".format(caseLabel, caseNumbers, deathLabel, deathNumbers, 
            recoverLabel, recoverNumber, "*"*20))

# Country wise fetching
def byCountry(country):
    uClient = requests.get("https://www.worldometers.info/coronavirus/#countries")
    src = uClient.content
    uClient.close()

    page = soup(src, 'html.parser')
    containers = page.findAll("div", {"class": "main_table_countries_div"})
    countriesContainers = containers[0].table.tbody.findAll("tr", {"style": ""})

    countries = []
    for i in range(len(countriesContainers)):
        countries.append(countriesContainers[i].td.text.strip().lower())

    data = []
    if country.lower() in countries:
        datas = countriesContainers[countries.index(country.lower())].findAll("td")
        for j in range(1,8):
            if datas[j].text.strip() == "":
                data.append("None")
            else:    
                data.append(datas[j].text.strip())
        print('''\nCORONA(COVID-19) CASES IN {0}
*********************

Total Cases:  {1}
New Cases:  {2}
Total Deaths:  {3}
New Deaths:  {4}
Total Recovered:  {5}
Active Cases:  {6}
Serious/Critical:  {7}'''.format(country.upper(), data[0], data[1], data[2], data[3], data[4], data[5], data[6]))        

# Check if Args passed or not
if len(sys.argv) > 1:
    byCountry(sys.argv[1].strip())
else:
    print("\nNo Countries Passed, Printing World Wide Details\n{}".format("-"*50))
    world()
