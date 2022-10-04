from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
#from django.http import Http404, HttpResponse

from bs4 import BeautifulSoup
import requests
#from PIL import Image
#import urllib.request
import os

from .doge_scraper import get_postings, extract_dog


# Create your views here.


def fetch_dog(request):
    def extract_dog(posting):
        div = posting.div
        if not div:
            return

        breed = posting.find("div", class_="list-animal-breed").text
        age = posting.find("div", class_="list-animal-age").text
        gender = posting.find("div", class_="list-animal-sexSN").text
        picture = posting.find('img', class_='list-animal-photo').get('src')



        months_text = age.strip(" months")
        months_int = int(months_text or 0)

        if months_int < 3 and "Australian" in breed and gender == "Male":
            return {
                "id": posting.find("div", class_="list-animal-id").text,
                "url": (
                    "http://ws.petango.com/webservices/adoptablesearch/"
                    + div.a.get("href")
                ),
                "name": posting.find("div", class_="list-animal-name").text,
                "breed": breed,
                "age": months_int,
                "gender": gender,
                "picture": picture
            }


    def get_postings():
        page = requests.get(
            "https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimal"
            "s.aspx?species=Dog&gender=A&agegroup=UnderYear&location=&site=&onhol"
            "d=A&orderby=name&colnum=3&css=http://ws.petango.com/WebServices/adop"
            "tablesearch/css/styles.css&authkey=io53xfw8b0k2ocet3yb83666507n2168t"
            "af513lkxrqe681kf8&recAmount=&detailsInPopup=No&featuredPet=Include&s"
            "tageID=&wmode=opaque"
        )
        source = page.content
        soup = BeautifulSoup(source, "lxml")
        #images = soup.find_all("div", class_="list-animal-photo-block")
        postings = soup.find_all("td", class_="list-item")
        return postings




    postings = get_postings()
    dogs = [
        extract_dog(posting) for posting in postings
        if extract_dog(posting) is not None
    ]

    #def organize_dogs(dogs):
    record_strings = [
        (
            f"Name: {record['name']}\nBreed: {record['breed']}\nAge (Months):"
            f" {record['age']}\nGender: {record['gender']}\nURL: "
            f"{record['url']}\nPicture: {record['picture']}"
        )

    for record in dogs
    ]

    record_string = "\n\n".join(record_strings)



    return render(request, 'dogs/home.html', {'dogs': dogs})
