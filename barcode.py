from bs4 import BeautifulSoup
import requests

# class Barcode():
#     def __init__(self, barcode):
#         url = "https://barcode-list.com/barcode/EN/Search.htm?barcode="+str(barcode)
#         response = requests.get(url)
#         self.web_page = response.text

#     def find_barcode(self):
#         soup = BeautifulSoup(self.web_page, "html.parser")
#         list = soup.select(selector=".even td")
#         return list[2].text

class Barcode():
    def __init__(self, barcode):
        url = f"https://api.barcodelookup.com/v3/products?barcode={barcode}&formatted=y&key=daim9un33x3vgimtpntggbe0unuwqa"
        response = requests.get(url)
        self.product_data = response.json()

    def find_barcode(self):
        return self.product_data["products"][0]["title"]

        