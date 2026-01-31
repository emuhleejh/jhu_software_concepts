from urllib import parse, robotparser
from scrape import Scrape

agent = "student"
base_url = "https://www.thegradcafe.com/"
full_url = "https://www.thegradcafe.com/survey/"

parser = robotparser.RobotFileParser(base_url)
parser.set_url(parse.urljoin(base_url, "robots.txt"))
parser.read()
print(parser.can_fetch(agent,base_url))

website = Scrape(full_url,agent)
website.read_page()