from bs4 import BeautifulSoup
import requests
import numpy as np
from time import sleep
from random import randint
from pandas import DataFrame

"""
Each page url is set up as https://shop.tcgplayer.com/price-guide/pokemon/X, where X is the set for that page. To get a list of set names I will extract the
set names from the drop down menu that lets you select which set to view.
"""

response = requests.get('https://shop.tcgplayer.com/price-guide/pokemon/') # requesting response from initial page where set names will be extracted

soup = BeautifulSoup(response.text, 'html.parser')

# Use beautifulSoup to find drop down menu. 
drop_down = soup.find('select', {'class': "priceGuideDropDown", "id": "set"}).findAll('option')

# this will extract the "value" i.e. the set name from the drop down menu and place it in the list of pages
pages = [i.get("value") for i in drop_down]

# now that the set names are available in the pages list they can be used to parse through all url pages and extract pokemon data
# all data will be extracted into data = [] list
data = []

for page in pages: # for every page in pages list, i.e. for every set that is in pages

    # the requested page will be the URL + str(page) which will be the sets found in the pages list
    page = requests.get("https://shop.tcgplayer.com/price-guide/pokemon/" + str(page))
    
    soup2 = BeautifulSoup(page.text, 'html.parser')
    # right_table will find the specific table of interest in site HTML
    right_table = soup2.find("table", attrs={"class": "priceGuideTable tablesorter"})
    # right_table_data finds all table row elements in the table of interest, i.e. right_table
    right_table_data = right_table.tbody.find_all("tr")[0:]
    # don't want to burden the site with requests so randint will be used to space out requests
    sleep(randint(2, 20))

    for div in right_table_data:      # for every div in all table row elements
        row = ''                      # row = '' will help parse in next part of code
        rows = div.findAll('td')      # rows = each individual cell
        for row in rows:
            if row.find(text=True):   # for every '' in each individual cell find where text = true
                data.append(row.text.strip()) # and append that text to data list object, using strip() for cleanup 

data_list = [data[i:i+6] for i in range(0, len(data), 6)]  # changes data list into list of lists

df = DataFrame(data_list, columns=['card_name', 'card_rarity', 'card_number', 'market_price', 'median_price', 'view']) # convert to dataframe

df = df.drop(columns=['view']) # who needs view anyways

df['market_price'] = df['market_price'].map(lambda x: x.lstrip('$')) # cleaning up prices by dropping $
df['median_price'] = df['median_price'].map(lambda x: x.lstrip('$'))

df['market_price'] = df['market_price'].replace('—', np.NaN) # replace — with NaN numeric type
df['median_price'] = df['median_price'].replace('—', np.NaN)
