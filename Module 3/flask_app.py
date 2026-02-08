# Necessary modules to operate programs
import os
import psycopg
from flask import Flask, render_template
from query_data import Query

page = Flask(__name__)

dbname = "applicants"
user = "postgres"
password = "python"

# Return 'home' html template when endpoint matches '/'
@page.route("/")

def home():
    q_data = Query(dbname, user, password)
    all_data = q_data.run_query()
    return render_template("home.html", data=all_data)

# Run application
if __name__ == "__main__":
    page.run(host="0.0.0.0", port=8080, debug=True)