import streamlit as st
import subprocess
import pandas as pd
import time

# Function to find the matching question and its corresponding answer
def find_matching_question(user_input, text_data):
    matching_question = None
    matching_answer = None
    for question, answers in text_data.items():
        if user_input.lower() == question.lower():
            matching_question = question
            matching_answer = answers[0]  # Assuming each question has only one answer
            break
    return matching_question, matching_answer

# Function to read job data from file
def read_job_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Error reading job data: {e}")
        return None

# Function to call webscrape.py with job role and location
def scrape_jobs(job_role, location):
    subprocess.run(["python", "drive-download-20240514T173802Z-001\glassdoorscape.py", job_role, location])

# Streamlit app
def main():
    st.title("Job Search Chatbot")

    # Read text data from file
    file_path = "drive-download-20240514T173802Z-001\smsm.txt"
    text_data = {}  # Store questions and answers in a dictionary
    with open(file_path, 'r') as file:
        current_question = None
        for line in file:
            line = line.strip()
            if line.startswith('Question:'):
                current_question = line[len('Question:'):].strip()
                text_data[current_question] = []  # Initialize an empty list of answers for the current question
            elif line.startswith('Answer:'):
                if current_question:
                    text_data[current_question].append(line[len('Answer:'):].strip())

    # Chat interface
    st.subheader("Chat Interface")
    user_input = st.text_input("You:", "")

    # Process user input
    if user_input:
        user_input = user_input.lower()  # Convert user input to lowercase for easier processing
        matched_question, matched_answer = find_matching_question(user_input, text_data)
        if matched_question:
            st.text_area("Chatbot:", value=matched_answer, disabled=True)
        elif "search a job" in user_input or "find a job" in user_input:
            st.text_area("Chatbot:", value="Please provide the following details for job search:", disabled=True)
            job_role = st.text_input("Job Role:")
            location = st.text_input("Location:")
            if st.button("Search"):
                if job_role and location:
                    st.text_area("Chatbot:", value="Searching for jobs...", disabled=True)
                    # Call the scrape_jobs function with job role and location
                    scrape_jobs(job_role, location)
                    time.sleep(20)
                    # Provide feedback to the user
                    job_data = read_job_data("job_data.xlsx")
                    if job_data is not None:
                        st.write(job_data)
                else:
                    st.text_area("Chatbot:", value="Please provide both job role and location.", disabled=True)
        else:
            st.text_area("Chatbot:", value="I don't understand that.", disabled=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()