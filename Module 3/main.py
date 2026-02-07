# For parsing authentication
from urllib import parse, robotparser
# For website scraping
from scrape import Scrape
# For data cleaning
from clean import Clean

# Global instances for parse auth, website scraping
agent = "student"
base_url = "https://www.thegradcafe.com"
full_url = "https://www.thegradcafe.com/survey"

# File to store and return basic scraped data
applicant_data = "applicant_data.json"

def main():
    # Create Scrape object from website
    website = Scrape(base_url, full_url, agent)
    # Read given number of entries on webpage
    website.scrape_data(40)

    # Format entries into JSON file
    with open(applicant_data, "w") as file:
        file.write(website.load_data())

    # Create Clean object from 'applicant_data' file
    clean_data = Clean(applicant_data)
    # Clean applicant data with local LLM
    clean_data.clean_data()

if __name__ == "__main__":
    # Set up parsing authentication specs for website
    parser = robotparser.RobotFileParser(base_url)
    parser.set_url(parse.urljoin(base_url, "robots.txt"))
    parser.read() 
    
    # Run program if auth succeeds, return error if auth fails
    if parser.can_fetch(agent,base_url) == True:
        print("Authentication succeeded. Proceeding with program.")
        main()
    else:
        print(f"Error: authentication failed. \
              Access denied for {agent} on {base_url}.")