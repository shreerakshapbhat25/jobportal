import streamlit as st
import subprocess
import pandas as pd
import time
from googletrans import Translator

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
    subprocess.run(["python", "glassdoorscape.py", job_role, location])

# Function to translate text
def translate_text(text, dest_lang):
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

# Streamlit app
def main():
    st.title("Job Search Chatbot")

    # Read text data from file
    file_path = "smsm.txt"
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
        translator = Translator()
        # Translate user input to English if not in English
        translated_input = translator.translate(user_input, dest='en').text.lower()
        
        matched_question, matched_answer = find_matching_question(translated_input, text_data)
        
        if matched_question:
            chat_response = matched_answer
            st.text_area("Chatbot:", value=chat_response, disabled=True)
        elif "search a job" in translated_input or "find a job" in translated_input:
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
                    job_data = read_job_data("job_data3.xlsx")
                    if job_data is not None:
                        st.write(job_data)
                else:
                    chat_response = "Please provide both job role and location."
                    st.text_area("Chatbot:", value=chat_response, disabled=True)
        else:
            chat_response = "I don't understand that."
            st.text_area("Chatbot:", value=chat_response, disabled=True)
    
    # Translation functionality
    if st.button("Translate"):
        if 'chat_response' in locals():
            lang_choice = st.selectbox("Choose language", ["Hindi", "Kannada"])
            if lang_choice:
                dest_lang = "hi" if lang_choice == "Hindi" else "kn"
                translated_text = translate_text(chat_response, dest_lang)
                st.text_area("Translated Text:", value=translated_text, disabled=True)
        else:
            st.error("No chat response to translate.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
