from playwright.sync_api import sync_playwright
import time
import os
import logging
from urllib.parse import urljoin
from .helper import save_to_csv

LOG_DIR="logs"
LOG_FILE=os.path.join(LOG_DIR,"errors.log")
os.makedirs(LOG_DIR,exist_ok=True)
logging.basicConfig(
    filemode='w',
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
def scrape(keyword):
    base_url="https://www.guru.com/d/jobs/"
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        page=browser.new_page()
        page.goto(base_url)
        time.sleep(3)
        try:
            cookie_btn=page.wait_for_selector("button[id='onetrust-accept-btn-handler']")
            cookie_btn.click()
            logging.info("Cookie accepted")
        except:
            logging.error("Cookie btn not found")
        try:
            search_input=page.wait_for_selector("input[id='typeahead-34']")
            search_input.fill(keyword)
            search_input.press("Enter")
            logging.info(f"Search for {keyword}")
        except:
            logging.error("Search issue")
        time.sleep(5)
        
        all_jobs=[]
        try:
            jobs=page.query_selector_all("//*[@id='search-app']/div/section/div/div[2]/div/ul/li")
        except Exception as e:
            logging.error(f"Failed to find jobs: {str(e)}")
            page.screenshot(path="debug.png")
            browser.close()
            return
        for job in jobs:
            try:
                title_element=job.query_selector("h2 a")
                title=title_element.inner_text().strip()
                relative_url=title_element.get_attribute("href")
                url=urljoin(base_url,relative_url)
                
            except:
                title="N/A"
                url="N/A"
            try:                                       
                price=job.query_selector("div.jobRecord__budget span").inner_text().strip()
            except:
                price="N/A"
            all_jobs.append({
                "Job Title":title,
                "Price":price,
                "URL":url
            })
        browser.close()
    if all_jobs:
        save_to_csv(all_jobs, "guru.csv")
        return all_jobs
    else:
        logging.warning("No jobs found to save")
