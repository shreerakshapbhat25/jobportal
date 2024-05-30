from flask import Flask, request
import glassdoorscape

app = Flask(__name__)

@app.route('/scrape_jobs', methods=['POST'])
def scrape_jobs():
    job_role = request.form['job_role']
    location = request.form['location']
    glassdoorscape.scrape_and_combine(job_role, location)
    return 'Job data has been scraped and saved to an Excel file.'

if __name__ == '__main__':
    app.run(debug=True)