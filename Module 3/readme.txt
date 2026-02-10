# Name:
Emily Hammer (ehammer5)
 
## Module Info:
Module 3 Assignment
Database Queries Assignment Experiment
Due February 8, 2026 at 11:59 p.m. EST
 
## Approach:
### scrape.py
Module creates class Scrape that requires input of the base URL of the website to be scraped, the full URL of the specific page on the website that contains the data to be scraped, and the agent requesting to access the URL. It also initializes with an empty list to hold all results of the scraped webpage. 
Class method scrape_data() requires unique ID of most recent entry collect, then collects information from the page until it reaches the one with the given unique ID. It sets up a state machine to control which 'if' statement is executed for each row entry in the page's table, the regex pattern to be used to identify the program term from the entry, and the page number of results to start on. While loop executes until the number of results in the results list equals the requested number of entries from the method call. In while loop, method uses urllib.request and bs4 libraries to open and process the page by finding the entries table and each entry row. For loop iterates through each entry ('applicant') on the page and uses state machine to and quantity of data points in a row to control which 'if' statement is executed for the row. For each parent row (main row for a single applicant entry), method creates a new Student object and adds to Scrape objects results list. The parent row and following rows for the same applicant are then parsed using bs4, regex, and string operations and assigned to the applicant's Student object properties. Once the while loop completes by fulfilling the requested number of entries, method call ends.
Class method load_data() converts Student objects in Scrape object results list to JSON by calling Student method format() on each Student, adding each result to a student_list(), and returning a JSON formatted string.

### student.py
Module creates class Student to store individual entries collected from thegradcafe.com/survey. Class method format() formats each Student property with its associated label in a JSON structure.

### clean.py
Module creates class Clean that requires input of a filename. Class method llm_clean() runs the file received at initialization through the local LLM to enhance the program and university for each entry in the file and exports the results to a txt file.

### load_data.py
Module defines function create_table() that requires input of a database name, and the username and password to access the data. It uses this information to connect to the database and create a table in the database with predefined column ids.
Module defines function load_data() that requires input of a database name, and the username and password to access the data. It connects to the given database and processes through a JSON file to add data from the file to the table created in create_table().

### query_data.py
Module creates class Query that requires input of the database to be worked with, and the username and password to access the data. It also initializes with empty variables to be filled in upon calculation. Class method run_query() connects to the given database and proceeds to run several queries with SQL on the database using the psycopg connection to postgresql. Once queries have been run, psycopg connection fully commits analysis and closes.

### flask_app.py
Program begins by importing necessary modules and setting global instances of variables for parsing authentication, website scraping, database interaction, and the file to store the scraped, unclean data. 
Program defines route '/' to the function home() which displays the series of questions and their answers based on the queries completed in query_data().
Program defines route '/pull-data/' to complete an authentication call and, if successful, connects to the database to grab the unique ID of the most recent entry recorded in the database thus far. It uses this unique ID to create a Scrape object and scrape data, then load the data into a file from which a Clean object is created. The Clean object runs the file through the local LLM and saves the results as a txt file, which is reformatted and loaded into the database.
Program defines route '/update-analysis/' to connect to the database and run all existing data through a Query object to complete updated queries before displaying it on the webpage.
Application declares main() and proceeds with an authentication call. If authentication is successful, main() runs as described. If authentication fails, application instead displays an error message to the user.
 
## Known bugs:
Loading data into database automatically updates the analysis on the webpage. Couldn't figure out how to disable buttons on webpage if a request to pull data was currently going.