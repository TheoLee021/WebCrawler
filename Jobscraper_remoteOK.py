import csv
import requests
from bs4 import BeautifulSoup

class JobScraper:
    def __init__(self, url, keywords):
        self.url = url
        self.keywords = keywords
        self.job_list = []
    # Print Results
    def show_jobs(self):
        print(self.job_list)

class RemoteOK(JobScraper):
    def __init__(self, url, keywords):
        super().__init__(url, keywords)

    # Scraping
    def scraping(self, url):
        print(f"Scapping {url}")
        response = requests.get(url, headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"})
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = soup.find("table", id = "jobsboard").find_all("tr", class_ = "job")
        for x in jobs:
            title = x.find("h2", itemprop = "title").text
            location = x.find("div", class_ = "location").text
            job_data = {
                "title": title,
                "location": location,
            }
            self.job_list.append(job_data)
            
    # Execute job scraping using each keyword
    def scrape_keyword(self):
        if isinstance(self.keywords, str):
            self.keywords = [self.keywords]

        for keyword in self.keywords:
            url_keyword = f"{self.url}/remote-{keyword}-jobs"
            self.scraping(url_keyword)
        
    # Exporting CSV
    def export_csv(self):
        with open("jobs.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Company", "Link"])

            for job in self.job_list:
                writer.writerow(job.values())

url = "https://remoteok.com"
keywords = ["flutter", "python", "golang"]

remoteok_scraper = RemoteOK(url, keywords)
remoteok_scraper.scrape_keyword()
remoteok_scraper.export_csv()
remoteok_scraper.show_jobs()