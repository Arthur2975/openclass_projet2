import requests
from bs4 import BeautifulSoup
import csv

#scrapper livre

def scrapper_livre (url_book):
    
    """
    docstring: cette fonction donn ç en entrée et ça en sortie
    """

    response = requests.get(url_book)

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        infos_book = []
        #faire plutot un dico

        #URL product
        infos_book.append(url_book)

        #UPC
        td = soup.find_all('td')
        upc = td[0].text
        infos_book.append(upc)
        
        #title

        title = soup.find('title')
        infos_book.append(title.text)

        #price with tax
        price_with_tax = td[3]
        infos_book.append(price_with_tax.text)

        #price without tax

        price_without_tax = td[2]
        infos_book.append(price_without_tax.text)

        #number_available
        number_available = td[5]
        infos_book.append(number_available.text)

        #product_description
        article  = soup.find_all('p')[3]
        infos_book.append(article.text)
        
    
        #category
        category = soup.find_all('a')[3].text
        infos_book.append(category)

        #review_rating
        review_rating = td[6]
        infos_book.append(review_rating.text)


        #image_url
        image_url = soup.find('img')
        infos_book.append(image_url)

        print(infos_book)

#scrapper catégorie

def scrapper_category(url_category):

    response_category = requests.get(url_category)

    soup_category = BeautifulSoup(response_category.text, 'lxml')

    #faire une boucle applicant le fn scrapper lire à chaque url de categorie

    for article in soup_category.find_all('article'):
        a = article.find_all('a')[0]
        url_incomplete_each_book = a.get('href')
        url_complete_each_book = url_incomplete_each_book.replace('../../..', 'http://books.toscrape.com/catalogue')
        scrapper_livre(url_complete_each_book)


    #exporter résultat dans un .csv


def csv():

    with open('category.csv', 'w', newline='') as csvfile:
        
        fieldnames = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_descriptioncategory', 'review_rating', 'image_url']

        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

        thewriter.writeheader()

        for info in infos_book:
            thewriter.writerow({''})


if __name__ == 'main':

    #scrapper site

    url_site = 'https://books.toscrape.com/index.html'

    response_site = requests.get(url_site)

    soup_site = BeautifulSoup(response_site.text, 'lxml')

    lis = soup_site.find_all('li')[2]

    for li in lis.find_all('li'):
        a = li.find('a')
        url_incomplete_categories = a.get('href')
        url_complete_categories = "http://books.toscrape.com/" + url_incomplete_categories
        scrapper_category(url_complete_categories)

    



# snake case
# variable de 3 lettres, exemple a devient link
# faire dico au lieu des listes

