from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request

import re
import json

from student import Student

class Scrape():
    def __init__(self, base, url, agent):
        # Base URL of website being searched
        self.base = base
        # Full URL of webpage to be searched
        self.url = url
        # Agent for auth
        self.agent = agent
        # Empty list to store results
        self.results = []

    def read_page(self, count):
        # Initiate state machine
        state = 1
        # Regex for program start term
        program_start_re = re.compile("[A-Za-z]*\s\d{4}")
        # Starting page of 'url' webpage being searched
        page_number = 1

        # Process webpage until number of results greater than requested count 
        while len(self.results) < count:

            # Read, parse webpage as html
            page_request = Request(self.url, headers={"User-Agent" : self.agent})
            page_read = urlopen(page_request)            
            page_html = page_read.read().decode("utf-8")
            soup = bs(page_html, "html.parser")

            # Locate table containing applicant entries
            table = soup.find("tbody")
            # Find all table rows
            entries = table.find_all("tr")

            # For each table row
            for entry in entries:
                data = entry.find_all("td")

                # Start of each new applicant's entry is known as 4 or more data points
                # 'Parent row' of applicant entry
                # Check if row has 4 or more data points
                if len(data) >= 4:
                    
                    # Reset state machine
                    state = 1
                    # Create new Student object
                    self.results.append(Student())
                    # Index of current Student object
                    i = len(self.results) - 1
                    
                    # Find University from table row
                    if data[0].find("div").find("div").string is not None:
                        self.university = data[0].find("div").find("div").string.strip()

                    # Find Program from table row
                    if data[1].find("span").string is not None:
                        self.program = data[1].find("span").string.strip()

                    # Set Program at Student object level based on contents of method variables
                    if self.university is not None:
                        if self.program is not None:
                            self.results[i].program = f"{self.program}, {self.university}"

                    elif self.program is not None:
                        self.results[i].program = f"{self.program}"

                    else:
                        self.results[i].program = "Unknown"

                    # Find and format table row data for Degree, set as Student property
                    if data[1].find("svg").next_sibling.next_sibling.string is not None:
                        self.results[i].degree = data[1].find("svg").next_sibling.next_sibling.string.strip()

                    # Find and format table row data for Date Added, set as Student property
                    if data[2].string.strip is not None:
                        self.results[i].date_added = data[2].string.strip()

                    # Find and format table row data for Results URL, set as Student property
                    self.results[i].results_url = self.base + data[4].find("a").get("href")
                    
                    # Store status information as 'applicant_status'
                    if data[3].find("div").string is not None:
                        self.results[i].applicant_status = data[3].find("div").string.strip().split(" ")

                        # Set 'applicant_status' and dates based on 'applicant_status' contents
                        if "Accepted" in self.results[i].applicant_status:
                            self.results[i].acceptance_date = f"{self.results[i].applicant_status[2]} {self.results[i].applicant_status[3]}"
                            self.results[i].applicant_status = "Accepted"

                        elif "Rejected" in self.results[i].applicant_status:                      
                            self.results[i].rejection_date = f"{self.results[i].applicant_status[2]} {self.results[i].applicant_status[3]}"
                            self.results[i].applicant_status = "Rejected"

                        elif "Interview" in self.results[i].applicant_status:
                            self.results[i].applicant_status = "Interview"

                        elif "Wait" in self.results[i].applicant_status:
                            self.results[i].applicant_status = "Wait listed"

                # Only run if row has a single data point and state is 2
                # 'Child row' of applicant entry
                elif len(data) == 1 and state == 1:
                    # Index of current Student object
                    i = len(self.results) - 1
                    
                    data_tag = data[0].find("div")
                    data_tags = data_tag.find_all("div")

                    # For each data point in row
                    for dt in data_tags:
                        # Generic format of data point
                        text = dt.string.strip()
                        
                        # Determine which pattern the data point fits
                        # Format and assign to corresponding Student object property
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
                    
                    # Update state machine for next parent elif
                    state = 2

                # Not all entries have comments
                # Only run if row has a single data point and state is 2
                # 'Child row' of applicant entry
                elif len(data) == 1 and state == 2:
                    # Index of current Student object
                    i = len(self.results) - 1

                    # Find comment in table row
                    data_comment = data[0].find("p")
                    # Only add comment to Student object if comment not empty
                    if data_comment is not None and data_comment.string is not None:
                        self.results[i].comments = data_comment.string.strip()

            # Update page number for pagination
            page_number += 1
            # Update 'url' to be next page
            self.url = self.base + f"/survey/?page={page_number}"

    # Format entire 'results' list of Student objects as JSON
    def serialize(self):
        student_list = []

        for result in self.results:
            student_list.append(result.format())

        return json.dumps(student_list)