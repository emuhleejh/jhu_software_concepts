# Name:
Emily Hammer (ehammer5)
 
## Module Info:
Module 2 Assignment
Web Scraping
Due February 1, 2026 at 11:59 p.m. EST
 
## Approach:
### scrape.py
Module creates class Scrape that requires input of the base URL of the website to be scraped, the full URL of the specific page on the website that contains the data to be scraped, and the agent requesting to access the URL. It also initializes with an empty list to hold all results of the scraped webpage. 
Class method read_page() requires input of number of entries to be collected, then collects information from the page for that number of entries to the website. It sets up a state machine to control which 'if' statement is executed for each row entry in the page's table, the regex pattern to be used to identify the program term from the entry, and the page number of results to start on. While loop executes until the number of results in the results list equals the requested number of entries from the method call. In while loop, method uses urllib.request and bs4 libraries to open and process the page by finding the entries table and each entry row. For loop iterates through each entry ('applicant') on the page and uses state machine to and quantity of data points in a row to control which 'if' statement is executed for the row. For each parent row (main row for a single applicant entry), method creates a new Student object and adds to Scrape objects results list. The parent row and following rows for the same applicant are then parsed using bs4, regex, and string operations and assigned to the applicant's Student object properties. Once the while loop completes by fulfilling the requested number of entries, method call ends.
Class method serialize() converts Student objects in Scrape object results list to JSON by calling Student method format() on each Student, adding each result to a student_list(), and returning a JSON formatted string.

### student.py
Module creates class Student to store individual entries collected from thegradcafe.com/survey. Class method format() formats each Student property with its associated label in a JSON structure.

### clean.py
Module creates class Clean that requires input of a filename. Class method llm_clean() runs the file received at initialization through the local LLM to enhance the program and university for each entry in the file and exports the results to a JSON file.
 
### main.py
Program begins by importing necessary modules and setting global instances of variables for parsing authentication, website scraping, and the file to store the scraped, unclean data. 
Function main() creates a Scrape object, then calls the method read_page(40000) to begin the scraping of the website for 40,000 entries and exports the results to a file 'applicant_data' as JSON by calling method serialize(). Function then creates Clean object from JSON file 'applicant_data' and runs the Clean object through method llm_clean().
Application declares main() and proceeds with an authentication call. If authentication is successful, main() runs as described. If authentication fails, application instead displays an error message to the user.
 
## Known bugs:
There are no known bugs.
 
## Citations:
https://beautiful-soup-4.readthedocs.io/en/latest/#