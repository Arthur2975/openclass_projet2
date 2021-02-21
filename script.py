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

url_category = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

response_category = requests.get(url_category)

soup_category = BeautifulSoup(response_category.text, 'lxml')

for article in soup_category.find_all('article'):
    print(article)
    '''
    url_books = article.get('href')
    url_whole = url_books.replace('../../..', 'http://books.toscrape.com/catalogue')  
    scrapper_book(url_whole)


print(scrapper_category('https://books.toscrape.com/catalogue/category/books/travel_2/index.html'))

#scrapper tout le site
'''
url_site = 'https://books.toscrape.com/index.html'

response_site = requests.get(url_site)

soup_site = BeautifulSoup(response_site.text, 'lxml')



#on a une def qui scrappe un livre
#on prend cette fonction pour scrapper tous les livres d'une catégorie en l'applicant à tous les url des livres
#on fait une fonction qui scrappe tous les livres d'une catégorie
#on utilise cette fonction en l'applicant à tous les url des categories




# créé un nouveau .csv sans que ca écrase le précédent à chaque boucle.

