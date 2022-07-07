# Züffaliger Anime des Tages 

## Auftrag
Der Auftrag für dieses Projekt war ein Skript mit Python schreiben, welches Daten über eine API in einem PDF gespeichert wird und diese als Email verschickt wird. Ich habe mich für die API namens Jikan entschieden, welche infos über Animes enthaltet.

## Beispiel Report
In meinem Programm werden mit der Hilfe eines API calls, Infos zu einem Zufälligen Animes, erhalten, gespeichert und diese in einem PDF gespreichert, welches als Mail und an den FTP Server hochgeladen wird. Der Report meines Programms besteht aus den folgenden Pünkten:
 * Ein Bild des Animes
 * Der Titel des Animes
 * Die Anzahl der Episoden
 * Die Genren des Anime
 * Eine Synopsis des Animes

## Ablauf
Am Anfang habe ich mich vorallem über den Auftrag informiert. Nachdem ich damit fertig geworden bin, habe ich mit der Suche nach einer Public API befasst. Hierbei habe ich diese Liste benutzt: https://github.com/public-apis/public-apis. Da ich öffters Anime schaue und es eine Abteilung von Anime APIs auf dieser Liste gibt, kam ich auf die Idee einen Zufälligen Anime als Report zu benutzten. Ich habe mir die verschiedenen möglichkeiten möglicher Anime APIs angeschaut und kam auf die Entscheidung Jikan zu benutzten. Ein Hauptgrund dafür war, dass Jikan benutzterfreundlich ist und es ein einfach zu verstehendes Tutorial gibt. Ich habe als nächstes meine IDE (Entwicklungs Umgebung) konfiguriert, damit ich meinen Python laufen lassen kann. Ich habe mich für die IDE Visual Studio Code entschieden, da ich mit dieser sehr bekannt bin. Nachdem ich meine IDE konfiguriert habe, hab ich anhand des Tutorials die ersten API Calls durchgeführt. Nachdem ich langsam das Gefühl für die API Calls in Python bekam, ging es recht schnell weiter. Zwischen diesem Zeitpunkt und dem Ende, bin ich praktisch auf keine Fehler gestossen.

## Code
Mein Code besteht aus mehreren Abschnitten und diese werde ich jetzt beschreiben. Hirbei wird das .env File ausgelassen, da diese private Angaben enthaltet.
### Imports
Das sind alle Import, welche ich in meinem Program verwendet habe:  
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

### Lesen der .env Variablen
Wie oben schon erwähnt beutzte ich ein .env File um private Angaben zu speichern. Diese beziehen sich auf verwendung für das Senden der Email und das Hochladens auf den FTP Server. Für das Lesen der .env variablen benutzte ich das Packet dotenv.  
load_dotenv()  
user = os.getenv("USER")  
app_password = os.getenv("APP_PASSWORD") 
to = os.getenv("TO")  
  
ftp_address = os.getenv("FTP_ADDRESS")  
ftp_username = os.getenv("FTP_USERNAME")  
ftp_password = os.getenv("FTP_PASSWORD")  

### API Call
In diesem Abschnitt wird der API Call durchgeführt und die zurückgegebenen Daten formatiert. Da in Jikan Animes, die +18 sind, enthaltet, filtriere ich diese aus. Das mache ich indem ich den gleichen API Call ausführe, bis es nicht +18 ist.  
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
          
 ### Generierung des PDFs
 Als nächstes wird das PDF generiert und darin die Daten, die oben beim API Call definiert wurde eingegeben. Dafür werwende ich das Package FPDF.  
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

### Senden des Emails
Mit dem Package yagmail kann man ganz einfach, nachdem man ein paar änderungen an seinem Gamil Account gemacht hat, Emial mit Python versenden.  
subject = "random anime of the day"  
content = ["this is the random anime of " + str(today), pdf_name]  
  
with yagmail.SMTP(user, app_password) as yag:  
    yag.send(to, subject, content)  
    logging.info("Sent email successfully at " + str(today))  
    
### Upload auf FTP Server
Beim upload auf den FDP Server habe ich meinen eigenen, der auf blpaced gehostet wird entschiden. http://j0150w.bplaced.net/  
with FTP(host=ftp_address) as ftp:  
    ftp.login(user=ftp_username, passwd=ftp_password)  

  with open(pdf_name, 'rb') as file:  
        ftp.storbinary('STOR ' + "www/" + pdf_name, file)  
        ftp.quit()  
        logging.info(  
            "PDF is uploaded to FTP server successfully at " + str(today))  



## Reflexion
Ich bin zufriden mit dem Resultat meines Projektes. Da ich am Anfang einige Probleme hatte, habe ich viel Zeit verloren. Aus diesem Grund denke ich, dass ich besseren Code schreiben hätte können.

## Schätzung der Note
Da ich nicht gerade der schönste Code oder die beste Dekumentation geschrieben habe, dafür die Anforderungen für das Projekt trozdem erfüllt habe, denke ich, dass ich eine 4.5 in dieser Projektarbeit erhalten werde. Dabei könnte ich mich aber auch täuschen, da ich mir nicht sicher sind, ob ich die Dokumentation im richtigen Format geschrieben habe.
