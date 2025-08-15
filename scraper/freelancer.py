from playwright.sync_api import sync_playwright
import os
import time
from .helper import save_to_csv
from urllib.parse import urljoin
import logging
LOG_DIR="logs"
LOG_FILE=os.path.join(LOG_DIR,"errors.log")
os.makedirs(LOG_DIR,exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def scrape(keyword):
    url="https://www.freelancer.pk/jobs%3Ffeatured%3Dtrue"
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        page=browser.new_page()
        page.goto(url)
        time.sleep(4)
        try:
            search=page.wait_for_selector("input[id='keyword-input']")
            search.fill("web scrapping")
            search.press("Enter")
            logging.info(f"Successfuly search the {keyword}")
            time.sleep(5)
        except:
            logging.error("issue in search selector")        
        try:
            jobs=page.query_selector_all("div.JobSearchCard-item")
            logging.info("Locate the selector jobs post")
        except:
            logging.error("Error in jobs post")
        all_jobs=[]
        if jobs:
            for job in jobs:
                try:
                    title_element=job.query_selector("div.JobSearchCard-primary-heading a")
                    title=title_element.inner_text().strip()
                    ele_url=title_element.get_attribute("href")
                    job_url=urljoin(url,ele_url)
                except:
                    title="N/A"
                    job_url="N/A"
                try:
                    price=job.query_selector("div.JobSearchCard-secondary-price").inner_text().strip()
                except:
                    price="N/A"
                all_jobs.append({
                    "Job Title":title,
                    "Price":price,
                    "URL":url
                })
    
    if all_jobs:
        save_to_csv(all_jobs, "freelancer.csv")
        return all_jobs
    else:
        logging.warning("No jobs found to save")
