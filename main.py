import requests
from bs4 import BeautifulSoup
import csv342 as csv
import urllib.request


#scraper livre

def scrapper_livre (url_book):

    '''    
    Cette fonction prend en argument l'url de la page d'un livre du site books.toscrape.com et exrait les information relatives à ce livre contenues
    dans le code HTML de la page
    '''

    response = requests.get(url_book)

    if response.ok:
        
        soup = BeautifulSoup(response.text, 'lxml')
        infos_book = {}

        #URL product
        infos_book['url_book'] = url_book

        #UPC
        balise_td = soup.find_all('td')
        upc = balise_td[0].text
        infos_book['upc'] = upc
        
        #title
        title = soup.find('title')
        infos_book['title'] = title.text

        #price with tax
        price_with_tax = balise_td[3]
        infos_book['price_with_tax'] = price_with_tax.text

        #price without tax

        price_without_tax = balise_td[2]
        infos_book['price_without_tax'] = price_without_tax.text

        #number_available
        number_available = balise_td[5]
        infos_book['number_available'] = number_available.text

        #product_description
        product_description  = soup.find_all('p')[3]
        infos_book['product_description'] = product_description.text

        #category
        category = soup.find_all('a')[3].text
        infos_book['category'] = category

        #review_rating
        review_rating = balise_td[6]
        infos_book['review_rating'] = review_rating.text

        #image_url
        balise_img = soup.find('img')
        image_url_incomplete = balise_img.get('src')
        image_url = image_url_incomplete.replace('../..', 'http://books.toscrape.com')
        infos_book['image_url'] = image_url
        title_1 = title.text.replace('\n', '').replace(' ', '').replace('|', '').replace("'", '')
        urllib.request.urlretrieve(image_url, 'images/' + str(title_1) + '.jpg')

        return(infos_book)


#scraper catégorie


def scrapper_category(url_category):

    '''
    Cette fonction prend en argument l'url de la page d'une catégorie de livre du site 'books.toscrape.com' et exrait les url de tous les livres
    de la catégorie. Puis elle applique la fonction scrapper_livre à chaque url pour extraire les informations relatives à tous les livres de cette catégorie
    '''

    response_category = requests.get(url_category)

    soup_category = BeautifulSoup(response_category.text, 'lxml')
    
    list_book = []

    for article in soup_category.find_all('article'):
        a = article.find_all('a')[0]
        url_incomplete_each_book = a.get('href')
        url_complete_each_book = url_incomplete_each_book.replace('../../..', 'http://books.toscrape.com/catalogue')
        list_book.append(scrapper_livre(url_complete_each_book))

    #exporter au format .csv

    export_csv(list_book=list_book)

    #creer une liste de toutes les url des images/ creer une boucle for image in liste_image 

#scraper site

def main():

    '''
    les lignes de codes ci après permettent d'extraire les url de chaque catégorie de livre du site 'books.tocrape.com' et d'appliquer la fonction
    scraper_catégorie qui elle même applique à chaque url de livre la fonction scraper_livre. Le résultat étant d'extraire toutes les informations relatives
    à tous les livres de toutes les catégories du site.
    '''

    url_site = 'https://books.toscrape.com/index.html'

    response_site = requests.get(url_site)

    soup_site = BeautifulSoup(response_site.text, 'lxml')

    balise_li = soup_site.find_all('li')[2]

    for li in balise_li.find_all('li'):
        link = li.find('a')
        url_incomplete_categories = link.get('href')
        url_complete_categories = "http://books.toscrape.com/" + url_incomplete_categories
        scrapper_category(url_complete_categories)



def export_csv(list_book):

    '''
    fonction permettant de créer des fichers .csv au nom des categories de livre et comprenant pour chaque ligne un livre et les informations associées
    '''

    infos_book = list_book[0]
    category_name = infos_book['category']

    with open('categories/' + str(category_name) + '.csv', 'w') as csvfile:
        fieldnames = ['url_book', 'upc', 'title', 'price_with_tax', 'price_without_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL)
        
        writer.writeheader()
        for book in list_book:
            writer.writerow(book)


if __name__ == '__main__':
    main()


