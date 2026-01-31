import urllib.request
import mechanicalsoup

from bs4 import BeautifulSoup as bs
import requests
from student import Student
import re

class Scrape():
    def __init__(self, base, url, agent):
        self.base = base
        self.url = url
        self.agent = agent
        self.results = []

    def read_page(self):
        page = requests.get(self.url, headers={"User-Agent" : self.agent})
        soup = bs(page.content, "html.parser")

        table = soup.find("tbody")
        entries = table.find_all("tr")

        state = 1
        program_start_re = re.compile("[A-Za-z]*\s\d{4}")

        for entry in entries:
            data = entry.find_all("td")

            if len(data) >= 4:
                state = 1
                self.results.append(Student())
                i = len(self.results) - 1

                self.results[i].university = data[0].find("div").find("div").string.strip()
                self.results[i].program = data[1].find("span").string.strip()
                self.results[i].degree = data[1].find("svg").next_sibling.next_sibling.string.strip()
                self.results[i].date_added = data[2].string.strip()
                self.results[i].applicant_status = data[3].find("div").string.strip()

                self.results[i].results_url = self.base + data[4].find("a").get("href")

                if "Accepted" in self.results[i].applicant_status:
                    status_split = self.results[i].applicant_status.split(" ")
                    self.results[i].acceptance_date = f"{status_split[2]} {status_split[3]}"
                elif "Rejected" in self.results[i].applicant_status:
                    status_split = self.results[i].applicant_status.split(" ")
                    self.results[i].rejection_date = f"{status_split[2]} {status_split[3]}"

            elif len(data) == 1 and state == 1:
                i = len(self.results) - 1
                
                data_tag = data[0].find("div")
                data_tags = data_tag.find_all("div")

                for dt in data_tags:
                    text = dt.string.strip()

                    if program_start_re.match(text):
                        self.results[i].program_start = text

                    elif "American" in text or "International" in text:
                        self.results[i].location = text

                    elif "GPA" in text:
                        self.results[i].gpa = text.replace("GPA ","")

                    elif "GRE V" in text:
                        self.results[i].gre_v = text.replace("GRE V ","")

                    elif "GRE AW" in text:
                        self.results[i].gre_aw = text.replace("GRE AW ","")

                    elif "GRE" in text:
                        self.results[i].gre = text.replace("GRE ","")
                
                state = 2

            elif len(data) == 1 and state == 2:
                i = len(self.results) - 1

                data_comment = data[0].find("p")

                if data_comment is not None:
                    self.results[i].comments = data_comment.string.strip()


        for student in self.results:
            print(f"{student} \n")