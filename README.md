# IFOA exam data scraper
Extract IFoA exam pass marks and rates from their examiner reports into a clean CSV.

**Final output** CSV with information up to April 2025 exams in Outputs/clean_data.csv

Below is further information about the code.

--------------------------------------------------------------------------------------------------------------
This project uses the following python scripts to extract the information.

1. download_zips.py
Download all zip files from the IFOA's webpage.
Inputs: URL of IFoA page.
Outputs: Downloaded zips

2. unzip.py
Extract all the files within the zips, including the examiners reports
Inputs: Downloaded zips
Outputs: Files inside of zips

3. data_from_pdfs.py
Identify the relevant exanimers report PDFs and extract the pass mark and pass rate.
  PDFs are identified by searching the first page for the relevant dates and subject names. (Note IFoA sometimes makes and error on thier documents which may require manual editing)
  The information is extracted using regex to find the sentences with the relevant information. (Note IFoA may change this sentence in the future)

In addition there is a check to verify if PDFs for all possible combination of the dates and subjects are found. This can identify any issues in the code process to with the examiners report (eg CM1 April 2020 will give an error as there is no examiners report).

Inputs: File path for PDF, Names of subjects to include, Names of dates to include
Outputs: 
raw_data.csv - Includes information from all pdfs identified which fit the criteira. This my include duplicates or errors.
Initial_data_checks.csv - Check PDFs exist for all date–subject combinations 

4. data_cleanse.py
Tidy up the raw_data.csv file, including:
Manual updates
Remove duplicates (and check they hold the same value)
Remove errors
Correct Date format
Sort data by subject and date

Inputs: raw_data.csv, Names of subjects to include, Names of dates to include
Outputs: clean_data.csv, duplicates_info.csv

5. data_checks.py
Run checks on the final clean data, including:
Number of data items as expected
All subject-date combo included
Min/Max values

Inputs: clean_data.csv, Names of subjects to include, Names of dates to include
Outputs:
   
