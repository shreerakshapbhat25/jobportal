from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def extract_profile_data(linkedin_url):
    # Configure Chrome webdriver
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    service = Service(
        'path_to_chromedriver')  # Replace 'path_to_chromedriver' with the actual path to chromedriver executable
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to LinkedIn profile URL
        driver.get(linkedin_url)

        # Wait for profile data to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-heading-xlarge")))

        # Extract profile data
        profile_data = {}
        profile_data['name'] = driver.find_element(By.CLASS_NAME, "text-heading-xlarge").text.strip()
        profile_data['headline'] = driver.find_element(By.CLASS_NAME, "mt1").text.strip()
        profile_data['summary'] = driver.find_element(By.CLASS_NAME, "pv-about__summary-text").text.strip()
        # Add more profile data extraction as needed

        return profile_data
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()


def generate_resume(profile_data):
    pdf_file = 'resume.pdf'
    c = canvas.Canvas(pdf_file, pagesize=letter)
    c.setFont("Helvetica", 12)
    textobject = c.beginText(50, 750)
    content = f"Name: {profile_data['name']}\n"
    content += f"Headline: {profile_data['headline']}\n"
    content += f"Summary: {profile_data['summary']}\n"
    # Add more profile data to the resume content
    textobject.textLines(content)
    c.drawText(textobject)
    c.save()
    return pdf_file


def main():
    linkedin_url = input("Enter your LinkedIn profile URL: ")
    profile_data = extract_profile_data(linkedin_url)
    if profile_data:
        pdf_file = generate_resume(profile_data)
        print(f"Resume generated: {pdf_file}")
    else:
        print("Failed to generate resume.")


if __name__ == "__main__":
    main()
