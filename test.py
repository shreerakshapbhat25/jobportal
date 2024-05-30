from flask import Flask, render_template, request, send_file
import os
import webbrowser
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

app = Flask(__name__)

def create_resume_txt(data):
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    summary = data.get('summary')
    experience = zip(request.form.getlist('experience_job_title'), request.form.getlist('experience_duration'), request.form.getlist('experience_duration'))
    education = zip(request.form.getlist('education_institution'), request.form.getlist('education_degree'), request.form.getlist('education_field'),request.form.getlist('education_duration'))
    certifications = zip(request.form.getlist('certification_name'), request.form.getlist('certification_source'), request.form.getlist('certification_field'))
    skills = request.form.getlist('skills[]')

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"resume_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(f"Name: {name}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Phone: {phone}\n")
        f.write(f"Address: {address}\n")
        f.write(f"Summary: {summary}\n")
        f.write("Experience:\n")
        for exp in experience:
            f.write(f"Job Title: {exp[0]}\n")
            f.write(f"Duration: {exp[1]}\n")
            f.write(f"Work Summary: {exp[2]}\n")
        f.write("Education:\n")
        for edu in education:
            f.write(f"Institution: {edu[0]}\n")
            f.write(f"Degree: {edu[1]}\n")
            f.write(f"Field of Study: {edu[2]}\n")
            f.write(f"Duration: {edu[3]}\n")
        f.write("Skills:\n")
        for skill in skills:
            f.write(f"- {skill}\n")
        f.write("Certifications:\n")
        for cert in certifications:
            f.write(f"Certificate Name: {cert[0]}\n")
            f.write(f"From: {cert[1]}\n")
            f.write(f"Field: {cert[2]}\n")

    print(f"Resume saved as {filename}")
    return filename

def txt_to_pdf(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.readlines()

    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)

    # Define styles for bold and underlined headings
    heading_style = ParagraphStyle(
        'Heading1',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=14,
        textColor=colors.black,
        spaceAfter=10,
        underline=True,
        underlineColor=colors.black
    )

    # Define style for regular text
    regular_style = ParagraphStyle(
        'Regular',
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        spaceAfter=5,
        textColor=colors.black
    )

    # Create a list to store PDF elements
    pdf_elements = []

    # Add content to PDF with appropriate styles
    for line in content:
        if line.strip() == "Name:" or line.strip() == "Skills:" or line.strip() == "Summary:" or line.strip() == "Experience:" or line.strip() == "Education:" or line.strip() == "Certifications:":
            pdf_elements.append(Paragraph(line.strip(), heading_style))
        else:
            pdf_elements.append(Paragraph(line.strip(), regular_style))

    # Build the PDF document
    doc.build(pdf_elements)

    print(f"PDF generated: {output_file}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        txt_file = create_resume_txt(data)
        pdf_file = os.path.splitext(txt_file)[0] + ".pdf"
        txt_to_pdf(txt_file, pdf_file)
        open_pdf = request.form.get('open_pdf')
        if open_pdf == 'yes':
            webbrowser.open_new(pdf_file)
        return render_template('index.html', resume_file=pdf_file)
    return render_template('index.html')

@app.route('/download/<filename>', methods=['GET'])
def download_resume(filename):
    resume_file = os.path.join(os.getcwd(), filename)
    return send_file(resume_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
