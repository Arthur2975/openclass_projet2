import requests
from bs4 import BeautifulSoup
import csv

#scraper livre

def scrapper_livre (url_book):
    
    
    # Cette fonction prend en argument l'url de la page d'un livre du site books.toscrape.com et exrait les information relatives à ce livre contenues
    # dans le code HTML de la page
    

    response = requests.get(url_book)

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        infos_book = []
        #faire plutot un dico

        #URL product
        infos_book.append(url_book)

        #UPC
        balise_td = soup.find_all('td')
        upc = balise_td[0].text
        infos_book.append(upc)
        
        #title

        title = soup.find('title')
        infos_book.append(title.text)

        #price with tax
        price_with_tax = balise_td[3]
        infos_book.append(price_with_tax.text)

        #price without tax

        price_without_tax = balise_td[2]
        infos_book.append(price_without_tax.text)

        #number_available
        number_available = balise_td[5]
        infos_book.append(number_available.text)

        #product_description
        article  = soup.find_all('p')[3]
        infos_book.append(article.text)
        
    
        #category
        category = soup.find_all('a')[3].text
        infos_book.append(category)

        #review_rating
        review_rating = balise_td[6]
        infos_book.append(review_rating.text)


        #image_url
        balise_img = soup.find('img')
        image_url_incomplete = balise_img.get('src')
        image_url_complete = image_url_incomplete.replace('../..', 'http://books.toscrape.com')
        infos_book.append(image_url_complete)

        print(infos_book)


#scraper catégorie

def scrapper_category(url_category):

    # Cette fonction prend en argument l'url de la page d'une catégorie de livre du site 'books.toscrape.com' et exrait les url de tous les livres
    #de la catégorie. Puis elle applique la fonction scrapper_livre à chaque url pour extraire les informations relatives à tous les livres de cette catégorie

    response_category = requests.get(url_category)

    soup_category = BeautifulSoup(response_category.text, 'lxml')

    #faire une boucle applicant la fn scrapper lire à chaque url de categorie

    for article in soup_category.find_all('article'):
        a = article.find_all('a')[0]
        url_incomplete_each_book = a.get('href')
        url_complete_each_book = url_incomplete_each_book.replace('../../..', 'http://books.toscrape.com/catalogue')
        scrapper_livre(url_complete_each_book)


def csv():

    # exporter résultat dans .csv

    with open('category.csv', 'w', newline='') as csvfile:
        
        fieldnames = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_descriptioncategory', 'review_rating', 'image_url']

        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

        thewriter.writeheader()

        for info in infos_book:
            thewriter.writerow({''})


#scraper site

if __name__ == 'main':

    #les lignes de codes ci après permettent d'extraire les url de chaque catégorie de livre du site 'books.tocrape.com' et d'appliquer la fonction
    #scraper_catégorie qui elle même applique à chaque url de livre la fonction scraper_livre. Le résultat étant d'extraire toutes les informations relatives
    #à tous les livres de toutes les catégories du site.


    url_site = 'https://books.toscrape.com/index.html'

    response_site = requests.get(url_site)

    soup_site = BeautifulSoup(response_site.text, 'lxml')

    balise_li = soup_site.find_all('li')[2]

    for li in balise_li.find_all('li'):
        link = li.find('a')
        url_incomplete_categories = link.get('href')
        url_complete_categories = "http://books.toscrape.com/" + url_incomplete_categories
        scrapper_category(url_complete_categories)

scrapper_livre('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')


# variable de 3 lettres, exemple a devient link
# faire dico au lieu des liste