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
        for json_object in applicant_data:

            if validate_entry(c, json_object):
                if json_object["gpa"] == "":
                    json_object["gpa"] = "NULL"

                if gpa_re.match(json_object["gpa"]) is None:
                    json_object["gpa"] = "NULL"

                if json_object["gre"] == "":
                    json_object["gre"] = "NULL"

                if json_object["gre_v"] == "":
                    json_object["gre_v"] = "NULL"

                if json_object["gre_aw"] == "":
                    json_object["gre_aw"] = "NULL"

                query += f"INSERT INTO results \
                    VALUES (DEFAULT,\
                    '{json_object["program"].replace("'", "''")}', \
                    '{json_object["comments"].replace("'", "''")}',\
                    '{json_object["date_added"].replace("'", "''")}',\
                    '{json_object["url"].replace("'", "''")}',\
                    '{json_object["status"].replace("'", "''")}',\
                    '{json_object["term"].replace("'", "''")}',\
                    '{json_object["US/International"].replace("'", "''")}',\
                    {json_object["gpa"].replace("'", "''")},\
                    {json_object["gre"].replace("'", "''")},\
                    {json_object["gre_v"].replace("'", "''")},\
                    {json_object["gre_aw"].replace("'", "''")},\
                    '{json_object["degree"].replace("'", "''")}',\
                    '{json_object["llm-generated-program"].replace("'", "''")}',\
                    '{json_object["llm-generated-university"].replace("'", "''")}');"

        # Execute query string and close connections
        c.execute(query)
        connection.commit()
    c.close()
    connection.close()

def clear_data():
    """
    For testing; empties database.
    """
    connection = psycopg.connect(dbname = "test_database", user = "postgres", password = "python")
    with connection.cursor() as c:
        c.execute("DELETE FROM results;")
        connection.commit()

        c.close()

        connection.close()
