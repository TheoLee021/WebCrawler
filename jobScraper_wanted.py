from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import csv

class JobScraper:
    def __init__(self, url, keywords):
        self.url = url
        self.keywords = keywords
        self.jobs_db = []

    def show_jobs(self):
        print(self.jobs_db)
    
class Wanted(JobScraper):
    def __init__(self, url, keywords):
        super().__init__(url, keywords)

    # Scraping
    def scrape_page(self, search_url):
        print(f"Scrapping {search_url}...")
        # Access the website using playwright for Scroll
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(search_url)
            # Scroll down five times
            for i in range(5):
                time.sleep(1)
                page.keyboard.down("End")
            content = page.content()
        # End Playwright
        # Job Scraping using BS4
        soup = BeautifulSoup(content, "html.parser")
        jobs = soup.find_all("div", class_="JobCard_container__REty8")
        for job in jobs:
            link = f"{self.url}{job.find('a')['href']}"
            title = job.find("strong", class_="JobCard_title__HBpZf").text
            company_name = job.find("span", class_="JobCard_companyName__N1YrF").text
            job_data = {
                "title": title,
                "company_name": company_name,
                "link": link,
            }
            self.jobs_db.append(job_data)

    # Execute job scraping using each keyword
    def scrape_keyword(self):
        if isinstance(self.keywords, str):
            self.keywords = [self.keywords]

        for keyword in self.keywords:
            url_keyword = f"{self.url}/search?query={keyword}&tab=position"
            self.scrape_page(url_keyword)
        
    # Exporting CSV
    def export_csv(self):
        with open("jobs.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Company", "Link"])

            for job in self.jobs_db:
                writer.writerow(job.values())

# Creating an instance of jobScraper
url = "https://www.wanted.co.kr"
keywords = ["python"]

wanted_scraper = Wanted(url, keywords)
wanted_scraper.scrape_keyword()
wanted_scraper.export_csv()
wanted_scraper.show_jobs()