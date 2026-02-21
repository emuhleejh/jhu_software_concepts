"""
Module to scrape data from a given website.
"""

import sys
from os.path import dirname
from urllib.request import urlopen, Request
import re
import json

from bs4 import BeautifulSoup as bs

sys.path.append(dirname(__file__))

# Regex for program start term
program_start_re = re.compile(r"[A-Za-z]*\s\d{4}")
# Regex for GPA
gpa_re = re.compile(r"(\A\d?\.\d+\z|\A\d\z)")

class Scrape():
    """
    Scrape data from website

    :param base: Base URL of the webpage being searched
    :type base: str

    :param url: Full URL of the webpage being searched
    :type url: str

    :param agent: User accessing the webpage, used for authentication
    :type agent: str
    """
    def __init__(self, base, url, agent):
        # Base URL of website being searched
        self.base = base
        # Full URL of webpage to be searched
        self.url = url
        # Agent for auth
        self.agent = agent
        # Empty list to store results
        self.results = []

    def scrape_data(self, recent_entry):
        """
        Pull data from the webpage

        :param recent_entry: Unique ID of the most recent entry pulled from the webpage
        :param recent_entry: int
        """
        # Initiate state machine
        state = 1
        # Starting page of 'url' webpage being searched
        page_number = 1

        can_proceed = True

        # Process webpage until number of results greater than requested count
        while can_proceed is True:

            # Read, parse webpage as html
            page_request = Request(self.url, headers={"User-Agent" : self.agent})
            with urlopen(page_request) as page_read:
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

                    can_proceed = self.find_main_row(recent_entry, data)

                # Only run if row has a single data point and state is 2
                # 'Child row' of applicant entry
                elif len(data) == 1 and state == 1:
                    i = len(self.results) - 1

                    data_tags = self.parse_data_tags(data)
                    
                    self.results[i]["term"] = "NULL"
                    self.results[i]["US/International"] = "NULL"
                    self.results[i]["gpa"] = "NULL"
                    self.results[i]["gre_v"] = "NULL"
                    self.results[i]["gre_aw"] = "NULL"
                    self.results[i]["gre"] = "NULL"
                    self.results[i]["comments"] = "NULL"

                    for dt in data_tags:
                        self.find_more_info(dt)

                    # Update state machine for next parent elif
                    state = 2

                # Not all entries have comments
                # Only run if row has a single data point and state is 2
                # 'Child row' of applicant entry
                elif len(data) == 1 and state == 2:              
                    self.find_comments(data)

            # Update page number for pagination
            page_number += 1
            # Update 'url' to be next page
            self.url = self.base + f"/survey/?page={page_number}"

    def find_main_row(self, recent_entry, data):
        """
        Checks whether the function should collect data about the next entry. \
        
        :param uid: Unique ID of current entry being processed
        :type uid: int
        
        :param recent_entry: Unique ID of most recent entry in database
        :type recent_entry: int
        """
        valid = True

        uid = data[4].find("a").get("href").replace("/result/","")

        if recent_entry >= int(uid):
            valid = False

        else:
            # Create new Student object
            self.results.append({})

            # Index of current Student object
            i = len(self.results) - 1

            if data[1].find("span").string is not None and \
            data[0].find("div").find("div").string is not None:
                self.results[i]["program"] = f"{data[1].find("span").string}, \
                    {data[0].find("div").find("div").string}"

            elif data[1].find("span").string is not None:
                self.results[i]["program"] = f"{data[1].find("span").string}"

            else:
                self.results[i]["program"] = "Unknown"

            # Find and format table row data for Degree, set as Student property
            if data[1].find("svg").next_sibling.next_sibling.string is not None:
                self.results[i]["degree"] = \
                    data[1].find("svg").next_sibling.next_sibling.string.strip()

            # Find and format table row data for Date Added, set as Student property
            if data[2].string.strip is not None:
                self.results[i]["date_added"] = data[2].string.strip()

            # Find and format table row data for Results URL, set as Student property
            self.results[i]["url"] = self.base + data[4].find("a").get("href")

            # Store status information as 'applicant_status'
            if data[3].find("div").string is not None:
                self.parse_applicant_status(data)

        return valid

    def parse_applicant_status(self, data):
        """
        Parse applicant status.
        
        :param data: 
        :type data: 
        """

        # Index of current Student object
        i = len(self.results) - 1

        app_status = data[3].find("div").string.strip().split(" ")

        # Set 'status' and dates based on 'status' contents
        if "Accepted" in app_status:
            self.results[i]["acceptance_date"] = \
                f"{app_status[2]} {app_status[3]}"
            self.results[i]["status"] = "Accepted"

        elif "Rejected" in app_status:
            self.results[i]["rejection_date"] = \
                f"{app_status[2]} {app_status[3]}"
            self.results[i]["status"] = "Rejected"

        elif "Interview" in app_status:
            self.results[i]["status"] = "Interview"

        elif "Wait" in app_status:
            self.results[i]["status"] = "Wait listed"

    def parse_data_tags(self, data):
        """
        Parses data tags.
        
        :param data: Table row of data from entry
        :type data: tr
        """

        data_tag = data[0].find("div")
        data_tags = data_tag.find_all("div")
        return data_tags

    def find_more_info(self, dt):
        """
        Finds additional info from the entry.

        :param dt: Piece of data from entry
        :type dt: tr
        """

        # Index of current Student object
        i = len(self.results) - 1

        # Generic format of data point
        text = dt.string.strip()

        # Determine which pattern the data point fits
        # Format and assign to corresponding Student object property
        if program_start_re.match(text):
            self.results[i]["term"] = text

        elif "American" in text or "International" in text:
            self.results[i]["US/International"] = text

        elif "GPA" in text:
            gpa_full = text.replace("GPA ","")
            if gpa_re.match(gpa_full):
                gpa = float(gpa_full)
                self.results[i]["gpa"] = f"{gpa:01.2f}"
            else:
                self.results[i]["gpa"] = ""

        elif "GRE V" in text:
            self.results[i]["gre_v"] = text.replace("GRE V ","")

        elif "GRE AW" in text:
            self.results[i]["gre_aw"] = text.replace("GRE AW ","")

        elif "GRE" in text:
            self.results[i]["gre"] = text.replace("GRE ","")

    def find_comments(self, data):
        """
        Finds comments from the entry, if any.

        :param data: Table row of data from entry
        :type data: tr
        """

        i = len(self.results) - 1

        # Find comment in table row
        data_comment = data[0].find("p")
        # Only add comment to Student object if comment not empty
        if data_comment is not None and data_comment.string is not None:
            self.results[i]["comments"] = data_comment.string.strip()

    # Format entire 'results' list of Student objects as JSON
    def load_data(self):
        """
        Format list of objects as json-formatted string

        :return: json-formatted string of objects
        :rtype: str
        """

        return json.dumps(self.results)
