import re
from PyPDF2 import PdfReader

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to identify name, email, and phone number from the extracted text
def extract_contact_info(text):
    # Regular expressions to extract name, email, and phone number
    name_pattern = re.compile(r'([A-Za-z\s]+)', re.IGNORECASE)
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone_pattern = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')

    # Search for name, email, and phone number in the text
    name_match = re.search(name_pattern, text)
    email_match = re.search(email_pattern, text)
    phone_match = re.search(phone_pattern, text)

    # Extract and format name, email, and phone number
    name = name_match.group(1).strip() if name_match else "Name not found"
    email = email_match.group().strip() if email_match else "Email not found"
    phone = phone_match.group().strip() if phone_match else "Phone number not found"

    return name, email, phone

# Function to extract skills from the resume text
def extract_skills(text):
    # Initialize an empty list to store extracted skills
    skills = []

    # Find the index of the "Skills:" heading
    skills_index = text.find("Skills:")

    if skills_index != -1:
        # Extract the text following the "Skills:" heading
        skills_text = text[skills_index + len("Skills:"):]

        # Split the text into lines
        lines = skills_text.split("\n")

        # Iterate through each line and extract the skill
        for line in lines:
            # Remove leading and trailing whitespace from each line
            line = line.strip()
            if line:
                if line == "Work Experience:":
                    break
                # Append the skill to the list
                skills.append(line)

    return skills

# Function to extract work experience from the resume text
def extract_work_experience(text):
    # Find the index of the "Work Experience:" heading
    start_index = text.find("Work Experience:")

    if start_index != -1:
        # Extract the text following the "Work Experience:" heading
        work_exp_text = text[start_index + len("Work Experience:"):]

        # Find the index of the next section or the end of the text
        end_index = work_exp_text.find("Education:") if "Education:" in work_exp_text else len(work_exp_text)

        # Extract the work experience text
        work_exp_text = work_exp_text[:end_index]

        # Replace "-" symbol with "\n" (newline character)
        work_exp_text = work_exp_text.replace("- ", "\n")

        return work_exp_text.strip()

    return "Work experience not found"

# Function to extract education details from the resume text
def extract_education(text):
    # Find the index of the "Education:" heading
    start_index = text.find("Education:")

    if start_index != -1:
        # Extract the text following the "Education:" heading
        education_text = text[start_index + len("Education:"):]

        # Find the index of the next section or the end of the text
        end_index = education_text.find("Work Experience:") if "Work Experience:" in education_text else len(education_text)

        # Extract the education text
        education_text = education_text[:end_index]

        # Remove leading and trailing whitespace from each line and remove empty lines
        education_text = '\n'.join(line.strip() for line in education_text.split('\n') if line.strip())

        return education_text.strip()

    return "Education not found"

# Function to generate a summary containing extracted information
def generate_summary(name, email, phone, skills, work_experience, education):
    summary = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nSkills: {', '.join(skills)}\n\nWork Experience:\n{work_experience}\n\nEducation:\n{education}"
    return summary

# Main function
def main():
    # Extract text from the resume PDF
    resume_text = extract_text_from_pdf("resume.pdf")

    # Extract contact information
    name, email, phone = extract_contact_info(resume_text)

    # Extract skills
    skills = extract_skills(resume_text)

    # Extract work experience
    work_experience = extract_work_experience(resume_text)

    # Extract education
    education = extract_education(resume_text)

    # Generate summary
    summary = generate_summary(name, email, phone, skills, work_experience, education)

    # Write summary to a text file
    with open("summary.txt", "w", encoding='UTF-8') as f:
        f.write(summary)

# Entry point of the script
if __name__ == "__main__":
    main()
