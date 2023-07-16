from dputils.scrape import Scraper, Tag
import pandas as pd
import os
from datetime import datetime

def data_miner_1(query = 'phones', page = 1):
    url = f'https://www.flipkart.com/search?q={query}&page={page}'
    print(url)
    scraper = Scraper(url)
    # page items
    target = Tag(cls='_1YokD2 _3Mn1Gg')
    items = Tag(cls='_1AtVbE col-12-12')
    # product items
    title = Tag(cls='_4rR01T')
    price = Tag(cls='_30jeq3 _1_WHN1')
    reviews = Tag('span', cls='_2_R_DZ')
    discount = Tag('div', cls='_3Ay6Sb')
    rating = Tag('div', cls='_3LWZlK')
    image = Tag('img', cls='_396cs4', output='src')
    out = scraper.get_all(target, items, name=title, price=price, reviews=reviews, discount=discount, rating=rating, image_url=image)
    return out

def data_miner_2(query = 'bags', page = 1):
    url = f'https://www.flipkart.com/search?q={query}&page={page}'
    scraper = Scraper(url)
    print(url)
    # page items
    target = Tag(cls='_1YokD2 _2GoDe3')
    items = Tag(cls='_1AtVbE col-12-12')
    # product items
    brand = Tag(cls='_2WkVRV')
    title = Tag('a',cls='IRpwTa')
    price = Tag(cls='_30jeq3')
    discount = Tag('div',cls='_3Ay6Sb')
    image_url = Tag('img', cls='_2r_T1I', output='src')
    out = scraper.get_all(target, items, brand=brand, name=title, price=price, discount=discount, image_url=image_url)
    return out

def save_data(data:list , filename="data.csv"):
    if not os.path.exists('datasets'):
        os.mkdir('datasets')
    if len(data) == 0:
        return print('No data to save')
    else:
        time = datetime.strftime(datetime.now(), '_%Y_%m_%d')
        filepath = os.path.join('datasets', f'{filename.lower()}{time}.csv')
        df = pd.DataFrame(data)
        # drop empty rows
        df = df.dropna()
    
        df.to_csv(filepath, index=False)
        return filepath
    

if __name__ == '__main__':
    data1 = []
    query ='phones'
    page = 1
    while True:
        page_data = data_miner_1(query, page)
        if len(page_data) == 0:
            break
        page += 1
        print(f'Page {page} data collected')
        data1.extend(page_data)

    filepath = save_data(data1, filename=query)
    print(f'Data saved at {filepath}')