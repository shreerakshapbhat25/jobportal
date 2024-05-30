import os
import subprocess
import json
import logging
import sys

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('job-search.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    job_role = data['job_role']
    location = data['location']
    
    # Log the received data
    app.logger.debug(f'Received job role: {job_role}, location: {location}')
    
    # Specify the path to the glassdoor.py script
    glassdoor_script = r"D:\majorproject\drive-download-20240514T173802Z-001\glassdoor.py"
    
    python_executable = sys.executable  # This will get the path to the current Python executable
    
    # Log the paths being used
    app.logger.debug(f'Glassdoor script path: {glassdoor_script}')
    app.logger.debug(f'Using Python executable: {python_executable}')
    
    # Run the glassdoor.py script with the job role and location
    result = subprocess.run([python_executable, glassdoor_script, job_role, location], capture_output=True, text=True)
    
    # Log the result of the subprocess
    app.logger.debug(f'Subprocess returned code: {result.returncode}')
    app.logger.debug(f'Subprocess stdout: {result.stdout}')
    app.logger.debug(f'Subprocess stderr: {result.stderr}')
    
    if result.returncode == 0:
    # Remove the first three lines from result.stdout
        lines = result.stdout.split('\n')[3:]
        filtered_stdout = '\n'.join(lines)
    
    # Log the filtered stdout
    app.logger.debug(f'Filtered subprocess output: {filtered_stdout}')
    
    if filtered_stdout:
        try:
            jobs = json.loads(filtered_stdout)
            app.logger.debug(f'Jobs data: {jobs}')
            return jsonify(success=True, jobs=jobs)
        except json.JSONDecodeError as e:
            app.logger.error(f'Error decoding JSON: {e}')
            return jsonify(success=False, error='Error decoding JSON')
    else:
        app.logger.warning('Subprocess output is empty')
        return jsonify(success=False, error='Subprocess output is empty')


if __name__ == '__main__':
    app.run(debug=True)
