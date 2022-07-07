from pkg_resources import resource_filename
import requests
from fpdf import FPDF
from datetime import date
import urllib.request
from PIL import Image
import yagmail
import os
from dotenv import load_dotenv
from ftplib import FTP
import logging

# getting environment variables
load_dotenv()
user = os.getenv("USER")
app_password = os.getenv("APP_PASSWORD")
to = os.getenv("TO")

ftp_address = os.getenv("FTP_ADDRESS")
ftp_username = os.getenv("FTP_USERNAME")
ftp_password = os.getenv("FTP_PASSWORD")


# request to api
isInappropriate = True
while isInappropriate:
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

    if "Hentai" not in data["genres"]:
        isInappropriate = False

# generating of pdf
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15)
urllib.request.urlretrieve(data["image"], "image.jpg")
image = Image.open(r"image.jpg")
image.save(r"image.png")
pdf.image(name="image.png")
pdf.cell(200, 10, txt="Title: " + data["title"], ln=1, align="L")
pdf.cell(200, 10, txt="Episodes: " + str(data["episodes"]), ln=1, align="L")
pdf.cell(200, 10, txt="Genres: " + ", ".join(data["genres"]), ln=1, align="L")
pdf.multi_cell(200, 10, txt="Synopsis: " + data["synopsis"], align="L",)
today = date.today()
pdf_name = "random_anime_of_" + str(today) + ".pdf"
pdf.output(pdf_name)

# sending email
subject = "random anime of the day"
content = ["this is the random anime of " + str(today), pdf_name]

with yagmail.SMTP(user, app_password) as yag:
    yag.send(to, subject, content)
    logging.info("Sent email successfully at " + str(today))

# upload pdf to ftp
with FTP(host=ftp_address) as ftp:
    ftp.login(user=ftp_username, passwd=ftp_password)

    with open(pdf_name, 'rb') as file:
        ftp.storbinary('STOR ' + "www/" + pdf_name, file)
        ftp.quit()
        logging.info(
            "PDF is uploaded to FTP server successfully at " + str(today))

logging.info("Script executed successfully at " + str(today))
