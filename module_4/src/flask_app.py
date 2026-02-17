# # Necessary modules to operate programs
# import psycopg
# from flask import Flask, render_template, Response
# from urllib import parse, robotparser

# from data_processing.query_data import Query
# from data_processing.load_data import load_data
# from data_processing.scrape import Scrape
# from data_processing.clean import Clean

# # Global instances for parse auth, website scraping
# agent = "student"
# base_url = "https://www.thegradcafe.com"
# full_url = "https://www.thegradcafe.com/survey"

# # File to store and return basic scraped data
# applicant_data = "applicant_data.json"

# dbname = "applicants"
# user = "postgres"
# password = "python"

# page = Flask(__name__)

# cache = {"pull-in-progress": False, "update-in-progress": False}

# # Return 'home' html template when endpoint matches '/'
# @page.route("/", methods=['GET', 'POST'])
# def home():
    # """
    # Homepage of Flask App showing questions and results from database queries

    # :return: Homepage template
    # :rtype: html
    # """
#     q_data = Query(dbname, user, password)
#     all_data = q_data.run_query()
#     return render_template("home.html", data=all_data)

# def run_parser():
#     parser = robotparser.RobotFileParser(base_url)
#     parser.set_url(parse.urljoin(base_url, "robots.txt"))
#     parser.read() 
    
#     # Run program if auth succeeds, return error if auth fails
#     if parser.can_fetch(agent,base_url) == True:
#         cache["pull-in-progress"] = True
#         print("Authentication succeeded. Proceeding with program.")

#         # Connect to database
#         connection = psycopg.connect(dbname = dbname, 
#                                 user = user, 
#                                 password = password)
        
#         # Grab most recent entry collected from website
#         with connection.cursor() as c:
#             c.execute("""SELECT MAX(NULLIF(regexp_replace(url, '\D','','g'), '')::numeric) AS result
#                         FROM   results;
#                     """)
#             row = c.fetchone()
#             most_recent_entry = int((row[0]))
            
#         # Create Scrape object from website
#         website = Scrape(base_url, full_url, agent)
#         # Read given number of entries on webpage
#         website.scrape_data(most_recent_entry)
        
#         # Format entries into JSON file
#         with open(applicant_data, "w") as file:
#             file.write(website.load_data())

#         # Create Clean object from 'applicant_data' file
#         clean_data = Clean(applicant_data)
#         # Clean applicant data with local LLM
#         clean_data.clean_data()

#         # Format txt file as json in memory
#         with open("llm_extend_applicant_data.txt", "r", encoding="utf-8") as file:
#             content = file.read()
#             content = content.replace("}", "},", content.count("}") - 1)        
#             formatted_json = "[" + content + "]"

#         # Write json memory to json file
#         with open("llm_extend_applicant_data.json", "w") as file:
#             file.write(formatted_json)

#         # Load data into database
#         load_data(dbname, user, password)
                
#     else:
#         print(f"Error: authentication failed. \
#             Access denied for {agent} on {base_url}.")

#     cache["pull-in-progress"] = False


# # Proceed with scraping and processing sequence
# @page.route("/pull-data/", methods=['GET', 'POST'])
# def pull_data():
    # """
    # Initiate the sequence of scraping new data
    
    # :return: Homepage template
    # :rtype: html
    # """
#     if cache["pull-in-progress"]:
#         return Response("{'a':'b'}", status=409, mimetype='application/json')

#     run_parser()

#     return home()

# def update_query():
#     cache["update-in-progress"] = True
#     q_data = Query(dbname, user, password)
#     all_data = q_data.run_query()
#     cache["update-in-progress"] = False

#     return all_data
    

# # Analyze all scraped and processed data
# @page.route("/update-analysis/", methods=['GET', 'POST'])
# def update_analysis():
#     """
#     Update the analysis on the homepage to reflect recently pulled data
    
#     :return: Homepage template
#     :rtype: html
#     """
#     # Process data through queries
#     if cache["update-in-progress"] is True or cache["pull-in-progress"] is True:
#         print(cache["pull-in-progress"])
#         return Response("{'a':'b'}", status=409, mimetype='application/json')

#     all_data = update_query()
    
#     return render_template("home.html", data=all_data)

# # Run application
# if __name__ == "__main__":
#     page.run(host="0.0.0.0", port=8080, debug=True)



# Necessary modules to operate programs
import psycopg
from flask import Flask, render_template, Response, Blueprint
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
bp = Blueprint("pages", __name__, template_folder = "templates")

dbname = "applicants"
user = "postgres"
password = "python"

cache = {"pull-in-progress": False, "update-in-progress": False}

def create_app():
    page = Flask(__name__)
    page.register_blueprint(bp)

    return page


# Return 'home' html template when endpoint matches '/'
@bp.route("/", methods=['GET', 'POST'])
def home():
    """
    Homepage of Flask App showing questions and results from database queries

    :return: Homepage template
    :rtype: html
    """
    q_data = Query(dbname, user, password)
    all_data = q_data.run_query()
    return render_template("home.html", data=all_data)

def run_parser():
    parser = robotparser.RobotFileParser(base_url)
    parser.set_url(parse.urljoin(base_url, "robots.txt"))
    parser.read() 
    
    # Run program if auth succeeds, return error if auth fails
    if parser.can_fetch(agent,base_url) == True:
        cache["pull-in-progress"] = True
        print("Authentication succeeded. Proceeding with program.")

        # Connect to database
        connection = psycopg.connect(dbname = dbname, 
                                user = user, 
                                password = password)
        
        # Grab most recent entry collected from website
        with connection.cursor() as c:
            c.execute("""SELECT MAX(NULLIF(regexp_replace(url, '\D','','g'), '')::numeric) AS result
                        FROM   results;
                    """)
            row = c.fetchone()
            most_recent_entry = int((row[0]))
            print(most_recent_entry)
            
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

        # Format txt file as json in memory
        with open("llm_extend_applicant_data.txt", "r", encoding="utf-8") as file:
            content = file.read()
            content = content.replace("}", "},", content.count("}") - 1)        
            formatted_json = "[" + content + "]"

        # Write json memory to json file
        with open("llm_extend_applicant_data.json", "w") as file:
            file.write(formatted_json)

        # Load data into database
        load_data(dbname, user, password)
        retrieving_data = False
                
    else:
        print(f"Error: authentication failed. \
            Access denied for {agent} on {base_url}.")
        retrieving_data = False

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
    cache["update-in-progress"] = True
    q_data = Query(dbname, user, password)
    all_data = q_data.run_query()
    cache["update-in-progress"] = False

    return all_data
    

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