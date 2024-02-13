# Resume Summarization Tool

***This Python program is a resume summarization tool that extracts information from resumes in PDF format and generates a summary containing contact information, skills, work experience, and education.***

### Code Explanation
``` import re
import spacy
from PyPDF2 
import PdfReader
```

- re: This module provides support for regular expressions in Python.
+ spacy: This library is used for natural language processing (NLP) tasks.
* PyPDF2: This library is used to extract text from PDF files.

```
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
```
- extract_text_from_pdf: This function takes the path to a PDF file as input and returns the text content of the PDF.

```
def extract_contact_info(text):
    name_pattern = re.compile(r'([A-Za-z\s]+)', re.IGNORECASE)
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone_pattern = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
    
    name_match = re.search(name_pattern, text)
    email_match = re.search(email_pattern, text)
    phone_match = re.search(phone_pattern, text)
    
    name = name_match.group(1) if name_match else "Name not found"
    email = email_match.group() if email_match else "Email not found"
    phone = phone_match.group() if phone_match else "Phone number not found"
    
    return name.strip(), email.strip(), phone.strip()
```
- extract_contact_info: This function extracts the candidate's name, email, and phone number from the resume text using regular expressions.

```
def extract_skills(text):
    skills = []
    
    skills_index = text.find("Skills:")
    
    if skills_index != -1:
        skills_text = text[skills_index + len("Skills:"):]
        lines = skills_text.split("\n")
        
        for line in lines:
            line = line.strip()
            if line:
                if line == "Work Experience:":
                    break
                skills.append(line)
    
    return skills
```
- extract_skills: This function extracts the candidate's skills from the resume text. It searches for the "Skills:" heading and extracts the skills listed below it.


```
def extract_work_experience(text):
    start_index = text.find("Work Experience:")
    
    if start_index != -1:
        work_exp_text = text[start_index + len("Work Experience:"):]
        end_index = work_exp_text.find("Education:") if "Education:" in work_exp_text else len(work_exp_text)
        work_exp_text = work_exp_text[:end_index]
        work_exp_text = work_exp_text.replace("- ", "\n")
        
        return work_exp_text.strip()
    
    return "Work experience not found"
```
- extract_work_experience: This function extracts the candidate's work experience from the resume text. It searches for the "Work Experience:" heading and extracts the text below it until the "Education:" heading or the end of the text.

```
def extract_education(text):
    start_index = text.find("Education:")
    
    if start_index != -1:
        education_text = text[start_index + len("Education:"):]
        end_index = education_text.find("Work Experience:") if "Work Experience:" in education_text else len(education_text)
        education_text = education_text[:end_index]
        education_text = '\n'.join(line.strip() for line in education_text.split('\n') if line.strip())
        
        return education_text.strip()
    
    return "Education not found"
```
- extract_education: This function extracts the candidate's education information from the resume text. It searches for the "Education:" heading and extracts the text below it until the "Work Experience:" heading or the end of the text.


```
def generate_summary(name, email, phone, skills, work_experience, education):
    summary = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nSkills: {', '.join(skills)}\n\nWork Experience:\n{work_experience}\n\nEducation:\n{education}"
    return summary
``` 
- generate_summary: This function generates a summary of the extracted information and formats it into a readable text format.

```
def main():
    resume_text = extract_text_from_pdf("resume.pdf")
    name, email, phone = extract_contact_info(resume_text)
    skills = extract_skills(resume_text)
    work_experience = extract_work_experience(resume_text)
    education = extract_education(resume_text)
    summary = generate_summary(name, email, phone, skills, work_experience, education)
    with open("summary.txt", "w") as f:
        f.write(summary)
```
- main: This is the main function of the program. It orchestrates the execution of the other functions, extracts information from the resume, generates a summary, and writes the summary to a text file named summary.txt.

## Usage


- Place the resumes you want to summarize in the same directory as the main.py file.
- Run the main.py script using Python:
  ``` python main.py ```
- The summarized information will be written to a file named summary.txt.

## Dependencies

```
- Python 3.x
- PyPDF2
- spaCy 
```

- Before running the program, make sure to install the required dependencies using the following command:

``` pip install PyPDF2 spacy ```

- Additionally, download the spaCy English model using the following command:

``` python -m spacy download en_core_web_sm ```

## @License

- This project is licensed under the MIT License. See the LICENSE file for details.