# Necessary modules to operate programs
import os
import psycopg
import json
from flask import Flask, render_template
# For parsing authentication
from urllib import parse, robotparser

from data_processing.query_data import Query
from data_processing.load_data import load_data
from data_processing.scrape import Scrape
from data_processing.clean import Clean

# Global instances for parse auth, website scraping
agent = "student"
base_url = "https://www.thegradcafe.com"
full_url = "https://www.thegradcafe.com/survey"

# File to store and return basic scraped data
applicant_data = "applicant_data.json"

dbname = "applicants"
user = "postgres"
password = "python"

page = Flask(__name__)

# Return 'home' html template when endpoint matches '/'
@page.route("/")
def home():
    q_data = Query(dbname, user, password)
    all_data = q_data.run_query()
    return render_template("home.html", data=all_data)

@page.route("/pull-data/")
def pull_data():
    print("Processing...")

    parser = robotparser.RobotFileParser(base_url)
    parser.set_url(parse.urljoin(base_url, "robots.txt"))
    parser.read() 
    
    # Run program if auth succeeds, return error if auth fails
    if parser.can_fetch(agent,base_url) == True:
        print("Authentication succeeded. Proceeding with program.")

        connection = psycopg.connect(dbname = dbname, 
                                  user = user, 
                                  password = password)
        
        with connection.cursor() as c:
            c.execute("""SELECT MAX(NULLIF(regexp_replace(url, '\D','','g'), '')::numeric) AS result
                        FROM   results;
                      """)
            
            row = c.fetchone()
            
            most_recent_entry = int((row[0]))
            
        # Create Scrape object from website
        website = Scrape(base_url, full_url, agent)
        # Read given number of entries on webpage
        website.scrape_data(most_recent_entry)
        
        # Format entries into JSON file
        with open(applicant_data, "w") as file:
            file.write(website.load_data())

        # Create Clean object from 'applicant_data' file
        clean_data = Clean(applicant_data)
        # Clean applicant data with local LLM
        clean_data.clean_data()

        with open("llm_extend_applicant_data.txt", "r") as file:
            content = file.read()
            content = content.replace("}", "},", content.count("}") - 1)        
            formatted_json = "[" + content + "]"

        with open("llm_extend_applicant_data.json", "w") as file:
            file.write(formatted_json)
                
    else:
        print(f"Error: authentication failed. \
              Access denied for {agent} on {base_url}.")

    return home()

@page.route("/update-analysis/")
def update_analysis():
    load_data(dbname, user, password)
    q_data = Query(dbname, user, password)
    all_data = q_data.run_query()
    print("Updating.")
    return render_template("home.html", data=all_data)

# Run application
if __name__ == "__main__":
    page.run(host="0.0.0.0", port=8080, debug=True)