"""
Module hosts functions to load data into database.
"""

#pylint: disable=e1101
# Above due to false-positive

import json
import re
import sys
from os.path import dirname

import psycopg

sys.path.append(dirname(__file__))

# Regex for GPA
gpa_re = re.compile(r"(\A\d?\.\d+\z|\A\d\z)")

APPLICANT_DATA_FILE = "llm_extend_applicant_data.json"

#SQL query to check if given entry is already in database
def validate_entry(cursor, json_object):
    """
    Confirm entry is not already in database

    :param cursor: Connection to database
    :type cursor: refcursor

    :param json_object: Entry to be checked for in database
    :type json_object: json

    :return: Determination whether the entry is unique
    :rtype: bool
    """

    query = f"SELECT 1 FROM results WHERE URL = '{json_object["url"]}'"
    cursor.execute(query)
    return cursor.fetchone() is None

# Load data from file into database
def load_data(dbname, user, password):
    """
    Load data from JSON file to database.
    
    :param dbname: Name of the database being accessed
    :type dbname: str

    :param user: Username to access the database
    :type user: str

    :param password: Password to access database with given username
    :type password: str
    """
    # Connect to database
    connection = psycopg.connect(dbname = dbname,
                                  user = user,
                                  password = password)

    with connection.cursor() as c:

          # Read file with entries for database
        with open(APPLICANT_DATA_FILE, "r", encoding="utf-8") as f:
            applicant_data = json.loads(f.read())

            # Empty query string
            query = ""

            # Format each entry in file as json object, append to query string
            params = {}
            i = 0
            for json_object in applicant_data:

                if validate_entry(c, json_object):
                    if json_object["gpa"] == "":
                        json_object["gpa"] = None

                    if gpa_re.match(json_object["gpa"]) is None:
                        json_object["gpa"] = None

                    if json_object["gre"] == "":
                        json_object["gre"] = None

                    if json_object["gre v"] == "":
                        json_object["gre v"] = None

                    if json_object["gre aw"] == "":
                        json_object["gre aw"] = None

                    query += f"INSERT INTO results \
                         VALUES(%(prog{i})s, \
                              %(comm{i})s, \
                              %(date_add{i})s,\
                              %(url{i})s,\
                              %(status{i})s,\
                              %(term{i})s,\
                              %(us_int{i})s,\
                              %(gpa{i})s,\
                              %(gre{i})s,\
                              %(gre_v{i})s,\
                              %(gre_aw{i})s,\
                              %(degree{i})s,\
                              %(llm_prog{i})s,\
                              %(llm_uni{i})s);"

                    params[f"prog{i}"] = json_object["program"]
                    params[f"comm{i}"] = json_object["comments"]
                    params[f"date_add{i}"] = json_object["date_added"]
                    params[f"url{i}"] = json_object["url"]
                    params[f"status{i}"] = json_object["status"]
                    params[f"term{i}"] = json_object["term"]
                    params[f"us_int{i}"] = json_object["US/International"]
                    params[f"gpa{i}"] = json_object["gpa"]
                    params[f"gre{i}"] = json_object["gre"]
                    params[f"gre_v{i}"] = json_object["gre v"]
                    params[f"gre_aw{i}"] = json_object["gre aw"]
                    params[f"degree{i}"] = json_object["degree"]
                    params[f"llm_prog{i}"] = json_object["llm-generated-program"]
                    params[f"llm_uni{i}"] = json_object["llm-generated-university"]

                    i+=1

        # Execute query string and close connections
        c.execute(query, params=params)
        connection.commit()
    c.close()
    connection.close()

def clear_data():
    """
    For testing; empties table.
    """
    connection = psycopg.connect(dbname = "test_database", user = "postgres", password = "python")
    with connection.cursor() as c:
        c.execute("DELETE FROM results;")
        connection.commit()

        c.close()

        connection.close()
