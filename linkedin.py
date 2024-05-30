from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import sys

def scrape_profiles():
    # Start the WebDriver and open the LinkedIn webpage
    driver = webdriver.Chrome()

    # Open the LinkedIn website
    driver.get("https://www.linkedin.com/")

    # Add your LinkedIn login code here if needed

    # Wait for the user to log in manually (if required)
    input("Press Enter after logging in to LinkedIn...")

    # Find the elements containing profile information
    profile_elements = driver.find_elements(By.CLASS_NAME, "vZOqEfUXVbsTnYwFmhbPlenvtPsKCQiho")

    profiles = []

    # Loop through profile elements and extract data
    for element in profile_elements:
        job_title = element.find_element(By.CSS_SELECTOR, ".t-bold").text
        company_name = element.find_element(By.CSS_SELECTOR, ".t-14.t-normal").text
        duration = element.find_element(By.CSS_SELECTOR, ".t-14.t-normal.t-black--light").text
        location = element.find_element(By.CSS_SELECTOR, ".t-14.t-normal.t-black--light").text
        description = element.find_element(By.CSS_SELECTOR, ".inline-show-more-text__link-container-collapsed").text

        profile_data = {
            "Job Title": job_title,
            "Company Name": company_name,
            "Duration": duration,
            "Location": location,
            "Description": description
        }

        profiles.append(profile_data)

    driver.quit()

    df = pd.DataFrame(profiles)
    df.to_excel("linkedin_profiles.xlsx", index=False)

if __name__ == "__main__":
    scrape_profiles()