import os
import fitz  # PyMuPDF
import pandas as pd
import regex as re

# Import list of subjects and dates
raw_data = pd.read_csv("Outputs/raw_data.csv")
subjects_csv = pd.read_csv("Inputs/subjects.csv", header=0)
dates_csv = pd.read_csv("Inputs/dates.csv", header=0)


# Remove first row, which is just index
raw_data = raw_data.iloc[:, 1:]
print(raw_data.head())


# ---------- Manually add in missing data -------------------------------

# Note - need to convert CM2 Sept 2020 from word to pdf

# Add in missing 2020 papers
cm1_sept20 = pd.DataFrame([{"Date": "April 2020", "Subject": "cm1", "Pass Mark": "Error", "Candidates Entered": "Error",
                            "Candidates Passed": "Error", "Pass Rate": "Error", "Filepath": "Error"}])
cm2_sept20 = pd.DataFrame([{"Date": "April 2020", "Subject": "cm2", "Pass Mark": "Error", "Candidates Entered": "Error",
                            "Candidates Passed": "Error", "Pass Rate": "Error", "Filepath": "Error"}])
cs1_sept20 = pd.DataFrame([{"Date": "April 2020", "Subject": "cs1", "Pass Mark": "Error", "Candidates Entered": "Error",
                            "Candidates Passed": "Error", "Pass Rate": "Error", "Filepath": "Error"}])
cs2_sept20 = pd.DataFrame([{"Date": "April 2020", "Subject": "cs2", "Pass Mark": "Error", "Candidates Entered": "Error",
                            "Candidates Passed": "Error", "Pass Rate": "Error", "Filepath": "Error"}])
sp6_sept20 = pd.DataFrame([{"Date": "April 2020", "Subject": "sp6", "Pass Mark": "Error", "Candidates Entered": "Error",
                            "Candidates Passed": "Error", "Pass Rate": "Error", "Filepath": "Error"}])

# Add in missing CB2 September 2023
cb2_sept23 = pd.DataFrame([{"Date": "september 2023",
                            "Subject": "cb2",
                            "Pass Mark": "62",
                            "Candidates Entered": "1115",
                            "Candidates Passed": "808",
                            "Pass Rate": float(808 / 1115),
                            "Filepath": "pdfs\\IandF_CB2_202309_Examiner%20Report.pdf"}])

updated_data = pd.concat([raw_data, cb2_sept23, cm1_sept20, cm2_sept20, cs1_sept20, cs2_sept20, sp6_sept20])


# --------- Remove duplicates ---------------------------------------
# Remove duplicates from main data
clean_data = updated_data.drop_duplicates(subset=["Date", "Subject"], keep="first")


# ---------- Identify duplicates and check they are identical ------------------
duplicates = updated_data[updated_data.duplicated(subset=["Date", "Subject"], keep=False)]

# Group duplicates by subject and date
# This saves them in a dictionary
grouped_duplicates = duplicates.groupby(["Subject","Date"])

# Iterate through the dictionary
# To check if the information is the same, check if there is only 1 unique item in the column
duplicates_info = []
for group_name, group_df in grouped_duplicates:
    check_list = [0, 0, 0]
    for i in range(2,5):
        check_list[i-2] = group_df.iloc[:,i].nunique() == 1

    duplicates_info.append({"Date": group_df.iloc[0,0],
                                "Subject": group_df.iloc[0,1],
                                "Number of duplicates": len(group_df),
                                "Match Pass Mark": check_list[0],
                                "Match Candidates Entered": check_list[1],
                                "Match Candidates Passed": check_list[2]})


# --------- Sort data -------------------------------------------

# Convert date to a format pandas can use
clean_data["Date"] = pd.to_datetime(clean_data["Date"])
sorted_data = clean_data.sort_values(by=["Subject", "Date"], ascending=[True, True])

# Covert errors into NaNs
columns = ["Pass Mark", "Candidates Entered", "Candidates Passed", "Pass Rate"]
sorted_data[columns] = sorted_data[columns].apply(pd.to_numeric, errors="coerce")


# -------- Print final data to CSV --------------------------------
sorted_data.to_csv('Outputs/clean_data.csv')

df_duplicates = pd.DataFrame(duplicates_info)
df_duplicates.to_csv('Outputs/duplicates_info.csv')