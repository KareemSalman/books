import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest

title_books = []
price_books = []
availability_books = []
rating_books = []
def get_page_content(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.content
        return None
    except:
        print("error")
        return None
    
def get_books(html , title_list , price_list , availability_books_list, rating_list):
    soup = BeautifulSoup(html , "lxml")
    books_containers = soup.find_all("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    for box in books_containers:
        # التقييم
        rating_tag = box.find("p" , {"class":"star-rating"})
        rating = rating_tag["class"][1]
        rating_list.append(rating)
        
        # العنوان
        title = box.find("h3").find("a")["title"]
        title_list.append(title)
        
        # السعر
        price = box.find("p" , {"class" : "price_color"}).text
        price_list.append(price)
        
        # التوافر
        availability_tag = box.find("p" , {"class" : "availability"})
        if availability_tag:
            availability = "Available" if "In stock" in availability_tag.text else "Out of Stock"
        else:
            availability = "Not Found"
        availability_books_list.append(availability)
        
def saving(title , price , availability , rating,file_name = "books_c.csv" ):
    file_list = [title , price , availability , rating]
    exported = zip_longest(*file_list)
    with open(file_name, "w", newline='', encoding='utf-8-sig') as file_books:
        wr = csv.writer(file_books, delimiter=';') 
        wr.writerow(["name", "price", "availability", "raiting"])
        wr.writerows(exported)
def main():
    title_books = []
    price_books = []
    availability_books = []
    rating_books = []
    page = 1
    while True:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        print(f"Scraping Page {page}...")
        html_content = get_page_content(url)
        if html_content is None:
            break
        get_books(html_content , title_books , price_books , availability_books , rating_books)
        page +=1
    saving(title_books , price_books , availability_books , rating_books)
if __name__ == "__main__":
    main()