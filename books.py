import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest

title_books = []
price_books = []
availability_books = []
rating_books = []

page = 1
while True:
    
    r = requests.get(f"https://books.toscrape.com/catalogue/page-{page}.html")
    
    if r.status_code != 200:
        print("تم الانتهاء من جميع الصفحات المتاحة.")
        break
        
    src = r.content
    soup = BeautifulSoup(src , "lxml")
    books_containers = soup.find_all("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    
    for box in books_containers:
        # التقييم
        rating_tag = box.find("p" , {"class":"star-rating"})
        rating = rating_tag["class"][1]
        rating_books.append(rating)
        
        # العنوان
        title = box.find("h3").find("a")["title"]
        title_books.append(title)
        
        # السعر
        price = box.find("p" , {"class" : "price_color"}).text
        price_books.append(price)
        
        # التوافر
        availability_tag = box.find("p" , {"class" : "availability"})
        if availability_tag:
            availability = "Available" if "In stock" in availability_tag.text else "Out of Stock"
        else:
            availability = "Not Found"
        availability_books.append(availability)

    # التعديل المهم هنا: بنزود الصفحة بعد ما نخلص الـ 20 كتاب
    print(f"Done page {page}")
    page += 1 
        
file_list = [title_books , price_books , availability_books , rating_books]
exported = zip_longest(*file_list)

with open("books_final.csv", "w", newline='', encoding='utf-8-sig') as file_books:
    wr = csv.writer(file_books, delimiter=';') 
    wr.writerow(["name", "price", "availability", "raiting"])
    wr.writerows(exported)
