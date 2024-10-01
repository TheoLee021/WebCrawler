import requests
from bs4 import BeautifulSoup

Job_List = []

class Scraping:
    def __init__(self, url):
        self.response = requests.get(url, headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"})
        soup = BeautifulSoup(self.response.content, "html.parser")
        jobs = soup.find("table", id = "jobsboard").find_all("tr", class_ = "job")
        for x in jobs:
            title = x.find("h2", itemprop = "title").text
            location = x.find("div", class_ = "location").text
            Job_List.append((title, location))

keyword = ["flutter", "python", "golang"]


for x in range(len(keyword)):
    url = f"https://remoteok.com/remote-{keyword[x]}-jobs"
    remote = Scraping(url)
    print(Job_List)