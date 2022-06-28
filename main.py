from pkg_resources import resource_filename
import requests
from fpdf import FPDF
from datetime import date
import urllib.request
from PIL import Image
import yagmail


# request to api
inappropriate = 1
while inappropriate == 1:
    url = "https://api.jikan.moe/v4/random/anime"
    r = requests.get(url=url)

    # konfiguration of data
    resData = r.json()["data"]
    genres = []
    for genre in resData["genres"]:
        genres.append(genre["name"])
    data = {
        "image": resData["images"]["jpg"]["image_url"],
        "title": resData["title"],
        "episodes": resData["episodes"],
        "genres": genres,
        "synopsis": resData["synopsis"]
    }
    if not data["genres"] == "Hentai":
        inappropriate = 0

# generating of pdf
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15)
urllib.request.urlretrieve(data["image"], "image.jpg")
image = Image.open(
    r"C:\Lehre\TBZ\Modul-122\LB2\Projekt\Modul-122_LB2\image.jpg")
image.save(r"C:\Lehre\TBZ\Modul-122\LB2\Projekt\Modul-122_LB2\image.png")
pdf.image(name="C:\Lehre\TBZ\Modul-122\LB2\Projekt\Modul-122_LB2\image.png")
pdf.cell(200, 10, txt="Title: " + data["title"], ln=1, align="L")
pdf.cell(200, 10, txt="Episodes: " + str(data["episodes"]), ln=1, align="L")
pdf.cell(200, 10, txt="Genres: " + ", ".join(data["genres"]), ln=1, align="L")
pdf.multi_cell(200, 10, txt="Synopsis: " + data["synopsis"], align="L",)
today = date.today()
pdf_name = "random_anime_of_" + str(today) + ".pdf"
pdf.output(pdf_name)

# generating email
user = "joelsow247@gmail.com"
app_password = "hhqdorjsbltycuih"
to = "joelsow247@gmail.com"

subject = "random anime of the day"
content = ["this is the random anime of " + str(today), pdf_name]

with yagmail.SMTP(user, app_password) as yag:
    yag.send(to, subject, content)
    print("Sent email successfully")
