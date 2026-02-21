"""
Run and host Flask webpage.
"""

#pylint: disable=e1101
# Above due to false-positive

#pylint: disable=e0401
# Above due to false-positive

import sys
from os.path import dirname
from urllib import parse, robotparser

# Necessary modules to operate programs
import psycopg
from flask import Flask, render_template, Response, Blueprint

from data_processing.query_data import Query
from data_processing.load_data import load_data
from data_processing.scrape import Scrape
from data_processing.clean import clean

sys.path.append(dirname(__file__))

# Global instances for parse auth, website scraping
AGENT = "student"
BASE_URL = "https://www.thegradcafe.com"
FULL_URL = "https://www.thegradcafe.com/survey"

# File to store and return basic scraped data
APPLICANT_DATA = "applicant_data.json"
CLEANED_FILE = "llm_extend_applicant_data.txt"
CLEANED_JSON = "llm_extend_applicant_data.json"
bp = Blueprint("pages", __name__, template_folder = "templates")

DBNAME = "applicants"
USER = "postgres"
PASSWORD = "python"

cache = {"pull-in-progress": False, "update-in-progress": False}

def create_app():
    """
    Start Flask webpage.
    """
    webpage = Flask(__name__)
    webpage.register_blueprint(bp)

    return webpage

# Return 'home' html template when endpoint matches '/'
@bp.route("/", methods=['GET', 'POST'])
def home():
    """
    Homepage of Flask App showing questions and results from database queries

    :return: Homepage template
    :rtype: html
    """
    q_data = Query(DBNAME, USER, PASSWORD)
    q_data.run_query()
    return render_template("home.html", data=q_data)

def get_most_recent_entry():
    """
    Get UID of most recent entry.
    """
    # Connect to database
    most_recent_entry = 0
    connection = psycopg.connect(dbname = DBNAME,
                            user = USER,
                            password = PASSWORD)

    # Grab most recent entry collected from website
    with connection.cursor() as c:
        c.execute(r"""SELECT MAX(NULLIF(regexp_replace(url, '\D','','g'), '')::numeric) AS result
                    FROM   results;
                """)
        row = c.fetchone()
        most_recent_entry = int((row[0]))
        # most_recent_entry = 1006103

    return most_recent_entry

def run_parser():
    """
    Run parser.
    """
    parser = robotparser.RobotFileParser(BASE_URL)
    parser.set_url(parse.urljoin(BASE_URL, "robots.txt"))
    parser.read()

    # Run program if auth succeeds, return error if auth fails
    if parser.can_fetch(AGENT,BASE_URL) is True:
        cache["pull-in-progress"] = True
        print("Authentication succeeded. Proceeding with program.")

        most_recent_entry = get_most_recent_entry()

        # Create Scrape object from website
        website = Scrape(BASE_URL, FULL_URL, AGENT)
        # Read given number of entries on webpage
        website.scrape_data(most_recent_entry)

        # Format entries into JSON file
        with open(APPLICANT_DATA, "w", encoding="utf-8") as file:
            file.write(website.load_data())

        # Clean applicant data with local LLM
        clean(APPLICANT_DATA)

        # Format txt file as json in memory
        with open(CLEANED_FILE, "r", encoding="utf-8") as file:
            content = file.read()
            content = content.replace("}", "},", content.count("}") - 1)
            formatted_json = "[" + content + "]"

        # Write json memory to json file
        with open(CLEANED_JSON, "w", encoding="utf-8") as file:
            file.write(formatted_json)

        # Load data into database
        load_data(DBNAME, USER, PASSWORD)

    else:
        print(f"Error: authentication failed. \
            Access denied for {AGENT} on {BASE_URL}.")

    cache["pull-in-progress"] = False

# Proceed with scraping and processing sequence
@bp.route("/pull-data/", methods=['GET', 'POST'])
def pull_data():
    """
    Initiate the sequence of scraping new data

    :return: Homepage template
    :rtype: html
    """
    if cache["pull-in-progress"]:
        return Response("{'a':'b'}", status=409, mimetype='application/json')

    run_parser()
    return home()

def update_query():
    """
    Update query.
    """
    cache["update-in-progress"] = True
    q_data = Query(DBNAME, USER, PASSWORD)
    q_data.run_query()
    cache["update-in-progress"] = False

    return q_data


# Analyze all scraped and processed data
@bp.route("/update-analysis/", methods=['GET', 'POST'])
def update_analysis():
    """
    Update the analysis on the homepage to reflect recently pulled data
    
    :return: Homepage template
    :rtype: html
    """
    # Process data through queries
    if cache["update-in-progress"] is True or cache["pull-in-progress"] is True:
        print(cache["pull-in-progress"])
        return Response("{'a':'b'}", status=409, mimetype='application/json')

    all_data = update_query()
    return render_template("home.html", data=all_data)

# Run application
if __name__ == "__main__":
    page = create_app()
    page.run(host="0.0.0.0", port=8080, debug=True)
