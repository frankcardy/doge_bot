import os
import smtplib

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import matplotlib.image as mpimg


def send_mail(records):
    record_strings = [
        (
            f"Name: {record['name']}\nBreed: {record['breed']}\nAge (Months):"
            f" {record['age']}\nGender: {record['gender']}\nURL: "
            f"{record['url']}\nPicture: {record['picture']}"
        )
        for record in records
    ]

    record_string = "\n\n".join(record_strings)
    subject = "Here are some doges you may be interested in"
    body = f"Check out the following links:\n\n{record_string}"

    msg = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("cardyf123@gmail.com", os.environ.get("EMAIL_PASSWORD"))
    server.sendmail(
        'franksdogs@gmail.com',
        'cardyf123@gmail.com',
        msg
    )
    server.quit()
    print("Email has been sent")


def extract_dog(posting):
    div = posting.div
    if not div:
        return

    breed = posting.find("div", class_="list-animal-breed").text
    age = posting.find("div", class_="list-animal-age").text
    gender = posting.find("div", class_="list-animal-sexSN").text
    picture = posting.find('img', class_='list-animal-photo').get('src')
    #img = mpimg.imread(picture)

    months_text = age.strip(" months")
    months_int = int(months_text or 0)

    if months_int < 3 and "Golden" in breed and gender == "Female":
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


if __name__ == "__main__":
    load_dotenv()
    postings = get_postings()
    dogs = [
        extract_dog(posting) for posting in postings
        if extract_dog(posting) is not None
    ]
    #print(len(dogs))
    if len(dogs) > 3:
        send_mail(dogs)
