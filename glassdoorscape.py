from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import sys
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font

def scrape_naukri_jobs(job_role, location):
    driver = webdriver.Chrome()
    driver.get("https://www.naukri.com/")
    time.sleep(3)

    try:
        job_role_input = driver.find_element(By.CSS_SELECTOR, ".suggestor-wrapper input[type='text'][placeholder='Enter skills / designations / companies']")
        job_role_input.send_keys(job_role)
        location_input = driver.find_element(By.CSS_SELECTOR, ".suggestor-wrapper input[type='text'][placeholder='Enter location']")
        location_input.send_keys(location)
        search_button = driver.find_element(By.CLASS_NAME, "qsbSubmit")
        search_button.click()
        resulting_url = driver.current_url
        jobs = []

        for i in range(1, 4):
            driver.get(resulting_url)
            time.sleep(3)
            job_tiles = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")

            for tile in job_tiles:
                job_title = tile.find_element(By.CLASS_NAME, "title").text
                company_name = tile.find_element(By.CLASS_NAME, "comp-name").text
                duration = tile.find_element(By.CLASS_NAME, "exp-wrap").text
                salary = tile.find_element(By.CLASS_NAME, "sal-wrap").text
                location = tile.find_element(By.CLASS_NAME, "loc-wrap").text
                url_element = tile.find_element(By.CLASS_NAME, "title")
                url = url_element.get_attribute("href")

                job_data = {
                    "Job Title": job_title,
                    "Company Name": company_name,
                    "Salary": salary,
                    "Location": location,
                    "URL": url
                }

                jobs.append(job_data)

        return jobs

    finally:
        driver.quit()

def scrape_glassdoor_jobs(job_role, location):
    driver = webdriver.Chrome()
    driver.get("https://www.glassdoor.co.in/Job/index.html")
    time.sleep(3)
    jobs = []

    try:
        job_role_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search keyword"]')
        job_role_input.send_keys(job_role)
        location_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search location"]')
        location_input.send_keys(location)
        location_input.send_keys(Keys.ENTER)
        time.sleep(5)
        job_cards = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__wjTHv")

        for i, card in enumerate(job_cards[:30], 1):
            job_title_element = card.find_element(By.CLASS_NAME, "JobCard_jobTitle___7I6y")
            job_title = job_title_element.text.strip()
            company_name_element = card.find_element(By.CLASS_NAME, "EmployerProfile_compactEmployerName__LE242")
            company_name = company_name_element.text.strip()
            location_element = card.find_element(By.CLASS_NAME, "JobCard_location__rCz3x")
            location = location_element.text.strip()
            try:
                salary_element = card.find_element(By.CLASS_NAME, "JobCard_salaryEstimate__arV5J")
                salary = salary_element.text.strip()
            except NoSuchElementException:
                salary = "Salary information not available"
            url_element = card.find_element(By.CLASS_NAME, "JobCard_jobTitle___7I6y")
            url = url_element.get_attribute("href")

            job_data = {
                "Job Title": job_title,
                "Company Name": company_name,
                "Salary": salary,
                "Location": location,
                "URL": url
            }

            jobs.append(job_data)

    except Exception as e:
        print("Error processing job card:", e)

    driver.quit()

    return jobs

def scrape_and_combine(job_role, location):
    naukri_jobs = scrape_naukri_jobs(job_role, location)
    glassdoor_jobs = scrape_glassdoor_jobs(job_role, location)
    combined_jobs = []
    min_len = min(len(naukri_jobs), len(glassdoor_jobs))

    for i in range(min_len):
        combined_jobs.append(naukri_jobs[i])
        combined_jobs.append(glassdoor_jobs[i])

    df = pd.DataFrame(combined_jobs)
    
    # Convert DataFrame to Excel with clickable URLs
    wb = Workbook()
    ws = wb.active
    ws.title = "Jobs"

    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)
            if c_idx == df.columns.get_loc("URL") + 1 and r_idx > 1:
                cell.hyperlink = value
                cell.font = Font(color="0000FF", underline="single")
    
    wb.save(r"job_data.xlsx")

if __name__ == "__main__":
    job_role = sys.argv[1]
    location = sys.argv[2]
    scrape_and_combine(job_role, location)