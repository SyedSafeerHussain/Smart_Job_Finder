from playwright.sync_api import sync_playwright
import time
import os
from urllib.parse import urljoin
from .helper import save_to_csv
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
    url="https://www.peopleperhour.com/freelance-jobs"
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        page=browser.new_page()
        page.goto(url)
        time.sleep(4)
        try:
            btn=page.wait_for_selector("//*[@id='cookie-banner']/div/div[2]/a")
            btn.click()
            logging.info("Cookie accept")
        except Exception as e:
            logging.error(f"cookie btn issue! {e}")
        try:
            search = page.wait_for_selector("input[placeholder='Search projects...']")
            search.fill(keyword)
            search.press("Enter")
            time.sleep(3)
            logging.info("Success in search keyword")
        except Exception as e:
            logging.error(f"Error in searching the keyword {e}")
        try:
            btn=page.wait_for_selector("//*[@id='cookie-banner']/div/div[2]/a")
            btn.click()
            logging.info("Cookie accept")
        except Exception as e:
            logging.error(f"Solved! {e}")    
        
        all_jobs=[]

        posts=page.query_selector_all("//*[@id='reactContainer']/div/div[3]/section/main/div/div[3]/div/div[2]/ul/li")
        
        for post in posts:
            try:
                title_element = post.query_selector("h6 a")
                title=title_element.inner_text().strip()
                url=title_element.get_attribute("href")
            except:
                title="N/A"
                url="N/A"
            try:
                price=post.query_selector("span[class='title-nano']").inner_text().strip()
            except:
                price="N/A"
            all_jobs.append({
                "Job Title":title,
                "Price":price,
                "URL":url
            })
        browser.close()    

    if all_jobs:
        save_to_csv(all_jobs, "pph.csv")
        return all_jobs
    else:
        logging.warning("No jobs found to save")