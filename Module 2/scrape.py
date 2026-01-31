import urllib.request
import mechanicalsoup

from bs4 import BeautifulSoup as bs
import requests
from student import Student

class Scrape():
    def __init__(self, url, agent):
        self.url = url
        self.agent = agent
        self.results = []

    def read_page(self):
        page = requests.get(self.url, headers={"User-Agent" : self.agent})
        soup = bs(page.content, "html.parser")

        table = soup.find("tbody")
        entries = table.find_all("tr")

        for entry in entries:
            data = entry.find_all("td")

            if len(data) >= 4:
                self.results.append(Student())
                index = len(self.results) - 1

                self.results[index].university = data[0].string
                self.results[index].program = data[1].string
                self.results[index].date_added = data[2].string
                self.results[index].applicant_status = data[3].string


        print(self.results)