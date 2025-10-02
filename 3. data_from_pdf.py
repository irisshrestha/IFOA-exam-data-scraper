import os
import fitz  # PyMuPDF
import pandas as pd
import regex as re

# Folder to get pdfs from
folder_name = "pdfs2"

# File all PDFs, even ones inside folders
pdf_files = []
for root, dirs, files in os.walk(folder_name):
    for file in files:
        if file.lower().endswith(".pdf"):
            pdf_files.append(os.path.join(root, file))

# Loop through all PDFs in the folder and convert to text
# Store info in list of dictionary
all_pdfs = []
for pdf_file in pdf_files:
    doc = fitz.open(pdf_file)
    page_text = doc[0].get_text().lower()
    # page_text = "\n".join(page.get_text() for page in doc)

    # Create a dictionary to save the filename and text
    all_pdfs.append({"location": pdf_file, "text": page_text})


# -------- Identify only the PDFs we want -----------------

# Import list of subjects and dates
subjects_csv = pd.read_csv("Inputs/subjects.csv", header=0)
dates_csv = pd.read_csv("Inputs/dates.csv", header=0)

# Set up the match criteria
# Check for "Examiners' report", subject name and date
exam_report = "EXAMINERS. REPORT"
subjects = [str(t).strip().lower() for t in subjects_csv["Subjects"].dropna()]
dates = [str(t).strip().lower() for t in dates_csv["Dates"].dropna()]

# Set up list to store in-scope PDFs
inscope_data = []

# Iterate through the dictionary, checking the text field
for dict in all_pdfs:
    text = dict["text"]
    exam_report_check = False
    subjects_check = False
    dates_check = False
    # Check for "Examiners' report"
    if re.search(exam_report, text.lower(), re.IGNORECASE):
        exam_report_check = True

        for subject in subjects:
            subjects_check = False
            for date in dates:
                dates_check = False
                # Check for subject name
                if subject in text.lower():
                    subjects_check = True
                    file_subject = subject

                    # Check for date
                    date_search = re.sub(" ", r"\\s*", date)
                    if re.search(date_search, text.lower(), re.IGNORECASE):
                        dates_check = True
                        file_date = date

                        # Store new information as a dictionary
                        if subjects_check == True and dates_check == True:
                            inscope_data.append({"location": dict["location"],
                                                 "Date": file_date,
                                                 "Subject": file_subject})

# Check which pdfs have been included and for duplicates
inscope_data_output = []
for subject in subjects:
    for date in dates:
        check = False
        counter = 0
        for dict in inscope_data:
            if dict["Date"] == date and dict["Subject"] == subject:
                check = True
                counter += 1
        inscope_data_output.append({"Date": date,
                                    "Subject": subject,
                                    "Check": check,
                                    "Counter": counter})


# ------- Extract the required information from the inscope PDFs --------------

# Set up patterns to search using regex
# The examiners' reports can have random spaces, commas in numbers etc, so need to account for this
pattern_passmark = re.compile(r"The.*Pass Mark.*? (\d+)", re.IGNORECASE)
pattern_numbers = re.compile(r"([\d,]+).*? presented themselves and ([\d,]+).*?passed", re.IGNORECASE)

all_data = []
for dict in inscope_data:
    pdf_file = dict["location"]
    file_date = dict["Date"]
    file_subject = dict["Subject"]
    doc = fitz.open(pdf_file)
    page_text = "\n".join(page.get_text() for page in doc)

    # Create a dictionary to save the filename and text
    match_passmark = pattern_passmark.search(page_text)
    match_numbers = pattern_numbers.search(page_text)

    passmark = int(match_passmark.group(1)) if match_passmark else "Error"
    num_candidates = int(match_numbers.group(1).replace(",", "")) if match_numbers else "Error"
    num_passed = int(match_numbers.group(2).replace(",", "")) if match_numbers else "Error"
    pass_rate = float(num_passed / num_candidates) if match_numbers else "Error"

    all_data.append({"Date": file_date,
                     "Subject": file_subject,
                     "Pass Mark": passmark,
                     "Candidates Entered": num_candidates,
                     "Candidates Passed": num_passed,
                     "Pass Rate": pass_rate,
                     "Filepath": pdf_file})


# -------- Print to CSV --------------------------------

df_check = pd.DataFrame(inscope_data_output)
df_check.to_csv('Outputs/Initial_data_checks.csv')

df = pd.DataFrame(all_data)
df.to_csv('Outputs/raw_data.csv')
