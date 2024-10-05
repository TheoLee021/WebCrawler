
#https://weworkremotely.com/remote-full-time-jobs

import requests
from bs4 import BeautifulSoup

url = "https://weworkremotely.com/remote-full-time-jobs"

response = requests.get(url)
#print(response.content)

soup = BeautifulSoup(
    response.content, "html.parser"
)

jobs = soup.find("div", id = "job_list").find_all("li")[1:-1] # <-cut the list, top&bottom useless

#print(jobs)

for job in jobs:
    title = job.find("span",class_="title").text
    company, position, region = job.find_all("span", class_="company")
    company = company.text
    position = position.text
    region = region.text
    print(title, company, position, region)
