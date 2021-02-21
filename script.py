import requests
from bs4 import BeautifulSoup

def scrapper_book(url_book):

    response = requests.get(url_book)

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
        infos_book.append(url_book)   

        #description
        description = soup.findAll('p')[3].text
        infos_book.append(description)
            
        #category
        category = soup.findAll('li')[2].text
        infos_book.append(category)

        print(infos_book)


#scrapper une categorie

def scrapper_category(url_category):

    response_category = requests.get(url_category)

    soup_category = BeautifulSoup(response_category.text, 'lxml')

    for article in soup_category.findAll('article'):    
        a = article.find('a')
        url_books = a.get('href')
        url_whole = url_books.replace('../../..', 'http://books.toscrape.com/catalogue')  
        scrapper_book(url_whole)


#scrapper tout le site

def scrapper_site(url_site):

    response_site = requests.get(url_site) 

    soup_site = BeautifulSoup(response_site.text, 'lxml')

    li_interessant = soup_site.findAll('li')[2]

    for li in li_interessant.findAll('li'):
        a = li.find('a')
        url_categories = a.get('href')
        url_final = ("https://books.toscrape.com/" + url_categories)
        scrapper_category(url_final)


scrapper_site('https://books.toscrape.com/index.html')


# créé un nouveau .csv sans que ca écrase le précédent à chaque boucle.



