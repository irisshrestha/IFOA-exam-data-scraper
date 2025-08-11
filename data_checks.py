import os
import fitz  # PyMuPDF
import pandas as pd
import regex as re

# Import list of subjects and dates
clean_data = pd.read_csv("Outputs/clean_data.csv")
subjects_csv = pd.read_csv("Inputs/subjects.csv", header=0)
dates_csv = pd.read_csv("Inputs/dates.csv", header=0)

# Remove first row, which is just index
clean_data = clean_data.iloc[:, 1:]

# Convert dates into same format for comparison
clean_data["Date"] = pd.to_datetime(clean_data["Date"]).dt.date
dates_csv["Dates"] = pd.to_datetime(dates_csv["Dates"]).dt.date

# ------- Check all expected exams are included -------------------------

# Check total count
actual_count = len(clean_data)
expected_count = len(subjects_csv) * len(dates_csv)
if actual_count == expected_count:
    print("Count as expected")
else:
    print("Count incorrect")

error_counter = 0
for subject in subjects_csv["Subjects"]:
    for date in dates_csv["Dates"]:
        check = False

        for actual_date, actual_subject in zip(clean_data["Date"], clean_data["Subject"]):
            if actual_date == date and actual_subject.lower() == subject.lower():
                check = True

        if not check:
            print(f"{subject} {date} is missing")
            error_counter += 1

if error_counter == 0:
    print("\nAll exams included")
else:
    print(f"{error_counter} exams missing")

# Check max and min values
max_passmark = clean_data["Pass Mark"].max()
max_entry = clean_data["Candidates Entered"].max()
max_passrate = clean_data["Pass Rate"].max()

print(f"\nMax Values: \n{clean_data.max()}")
print(f"\nMax Values: \n{clean_data.min()}")
