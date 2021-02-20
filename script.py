import requests
from bs4 import BeautifulSoup


url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = requests.get(url)

#infos à faire sortir: product page URL, UPC, title, price with taxes, price without taxes, 
#availability, description, category, review_rating, image_url

if response.ok:
    infos_book = []
    soup = BeautifulSoup(response.text, 'lxml')    
    
    #UPC, price tax inc, price tax exc, availability, reviews
    infos = soup.findAll('td')
    for info in infos:
        infos_book.append(info.text)

    #title
    title = soup.find('title')
    infos_book.append(title.text)

    #url image
    url_image = soup.find('img')
    infos_book.append(url_image)

    #url de la page
    infos_book.append(url)   

    #description
    description = soup.findAll('p')[3].text
    infos_book.append(description)
        
    #category
    category = soup.findAll('li')[2].text
    infos_book.append(category)

print(infos_book)

#lire en .csv

import csv
with open('tab.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

