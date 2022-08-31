#Imports the required libraries 
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import json



#I used https://jsonformatter.curiousconcept.com/ to read the json data clearly


#https://quakes.globalincidentmap.com was original  source but changed to https://m.emsc.eu

class seismic:
    def __init__(self):
        pass

    def fetchdata(self):
        #Makes a request to https://m.emsc.eu/webapp/get_earthquakes_list.php?type=full using headers to "mask" my computer as a "real" computer
        r = requests.get("https://m.emsc.eu/webapp/get_earthquakes_list.php?type=full", headers={'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.48", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}, timeout=None).text

        #Saves the data scraped from variable r as a json file format
        data = json.loads(r
                          )
        #Returns the latest earthquake
        return data["features"][0]["id"], data["features"][0]["properties"]["magnitude"]["mag"]
  


