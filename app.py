from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

def scrape_job_listings(location, keyword, job_type):
    # Initialize an empty list to store job URLs
    job_urls = []

    # Replace this URL with the actual job listing website you want to scrape
    base_url = "https://www.naukri.com"

    # Make a request to the job listing website
    response = requests.get(base_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # Find job listings based on the input keyword
        # You need to inspect the HTML structure of the job listing website to find the appropriate selectors
        job_elements = soup.find_all("div", class_="job")

        for job_element in job_elements:
            # Example logic to extract job URLs containing the keyword and matching job type
            job_title = job_element.find("h2").text
            job_url = job_element.find("a")["href"]
            job_category = job_element.find("span", class_="category").text

            if keyword.lower() in job_title.lower() and job_type.lower() in job_category.lower():
                job_urls.append(job_url)

    return job_urls

def create_excel(location, keyword, job_type):
    job_urls = scrape_job_listings(location, keyword, job_type)

    # Create a DataFrame to store the scraped job URLs
    df = pd.DataFrame({"Job URLs": job_urls})

    # Write the DataFrame to an Excel file
    excel_filename = "job_listings.xlsx"
    df.to_excel(excel_filename, index=False)

    return excel_filename

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    location = request.form["location"]
    keyword = request.form["keyword"]
    job_type = request.form["job_type"]

    excel_file = create_excel(location, keyword, job_type)
    return f"Excel file '{excel_file}' created successfully with scraped job listings."

if __name__ == "__main__":
    app.run(debug=True)