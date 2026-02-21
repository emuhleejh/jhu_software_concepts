Architecture
======================
Web Layer
-----------------------
This package includes a webpage which hosts a dynamic analysis of all data that has been pulled.
In addition to questions and their results, the webpage has two buttons: 
* Pull Data: Scrapes more data from Grad Cafe, processes it through an LLM, and loads it into the database.
* Update Analysis: Runs the database through a series of queries and displays the results on the webpage.

While either button is in a busy state, both buttons become temporarily disabled to allow the system time to complete its task.

Extract, Transform, Load Layer
-----------------------
The two buttons on the webpage interact with the website being scraped and the database.
When 'Pull Data' is clicked, the package scrapes more data from Grad Cafe, processes it through an LLM, and loads it into the PostgreSQL database.
When 'Update Analysis' is clicked, the package runs the database through a series of queries and displays the results on the webpage.

Database Layer
-----------------------
The PostgreSQL database holds all rows of data that have been scraped and cleaned by the package.
