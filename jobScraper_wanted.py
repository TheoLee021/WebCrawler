from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import csv

url = "https://www.wanted.co.kr"
keywords = ["python"]
jobs_db = []

def scrape_page(search_url):
    print(f"Scrapping {search_url}...")
    # Access the website using playwright for Scroll
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(search_url)
    # Scroll down five times
    for i in range(5):
        time.sleep(1)
        page.keyboard.down("End")

    content = page.content()
    p.stop()
    # End Playwright
    # Job Scraping using BS4
    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find_all("div", class_="JobCard_container__REty8")
    for job in jobs:
        link = f"{url}{job.find('a')['href']}"
        title = job.find("strong", class_="JobCard_title__HBpZf").text
        company_name = job.find("span", class_="JobCard_companyName__N1YrF").text
        job_data = {
            "title": title,
            "company_name": company_name,
            "link": link,
        }
        jobs_db.append(job_data)

# Execute job scraping by each keyword
for keyword in keywords:
    url_keyword = f"{url}/search?query={keyword}&tab=position"
    scrape_page(url_keyword)
    
# Display results
print(jobs_db)

# Exporting CSV
file = open("jobs.csv", "w")
writer = csv.writer(file)
writer.writerow(["Title", "Company", "Link"])

for job in jobs_db:
    writer.writerow(job.values())