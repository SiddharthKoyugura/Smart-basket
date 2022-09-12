import requests

URL = "https://api.sheety.co/8aec6271c1e06c070d513c708d4e5d9c/smartCartDemoDb/sheet1"

class Database():
    def __init__(self):
        response = requests.get(URL)
        self.items_data = response.json()

    def get_items_data(self):
        return self.items_data["sheet1"]

Database()