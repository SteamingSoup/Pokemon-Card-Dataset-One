from bs4 import BeautifulSoup
import requests
import numpy as np
from time import sleep
from random import randint
import pandas as pd
from pandas import DataFrame

url1 = 'https://pokemonprices.com/browse_sets'

response1 = requests.get(url1)

soup1 = BeautifulSoup(response1.text, 'html.parser')

table_select = soup1.findAll('table', {'class':"sortable", "id": "stats_list"})

sets = table_select[0].findAll('b')

sets = [[item.replace('<b>', '') for item in lst] for lst in sets]

sets_list = [item for sublist in sets for item in sublist]

final = []
for i in sets_list:
    j = i.replace(' ','+')
    final.append(j)
    
final_forreal = []
for i in final:
    j = i.replace('&', '%26')
    final_forreal.append(j)
    
    
data = []

for page in final_forreal:

    page = requests.get('https://pokemonprices.com/set/' + str(page))
    
    soup2 = BeautifulSoup(page.text, 'html.parser')
    
    title_table = soup2.find("table", {'id':'set_header'})
    
    card_table = soup2.find("table", {'class':"sortable", "id": "stats_list"})
    
    info = card_table.findAll('tr')
    
    sleep(randint(2,20))
    
    for td in info:
        row = ''
        rows = td.findAll('td')
        for row in rows:
            if(row.find(text = True)):
                data.append(row.text.strip())

    set_name = title_table.h3
    set_name.find(text = True)
    data.append(set_name.text.strip())
