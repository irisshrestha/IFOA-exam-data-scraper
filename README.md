# IFOA exam data scraper
This project extracts pass marks and pass rates from the IFoA examiners' reports and outputs the result into a structured CSV file.

**FINAL outputs** contains the final data and summary charts.


Below is further information about the code.

--------------------------------------------------------------------------------------------------------------
This project uses the following Python scripts to extract the information.

1. **download_zips.py**
Downloads all zip files from the IFOA's webpage.
    - Inputs: URL of IFoA page
    - Outputs: Downloaded zips

2. **unzip.py**
Extract all the files from the zips, including the examiners reports.

   - Inputs: Downloaded zips
   - Outputs: Files inside of zips

3. **data_from_pdfs.py**
Identify and extract information from the relevant examiners reports.

    PDFs are identified by searching the first page for the relevant dates and subject names. (Note: Some documents do not have this information on their front page and require manual inputs).
   
    The pass mark and pass rate is extracted using regex to find the sentences with the relevant information. (Note: IFoA may change this sentence in the future).
   
    There is a check to verify that examiners reports for all possible subject-date combinations are found. (eg CM1 April 2020 will give an error as there is no examiners report).
     
     - Inputs: File path for PDFs, list of subjects, list of dates  
     - Outputs:
       - raw_data.csv (Information from all PDFs which fit the criteira, which may include duplicates or errors)
       - Initial_data_checks.csv
         
4. **data_cleanse.py**
   Tidy up the raw_data.csv file, including:
   
    Applying manual updates,
    Remove duplicates (and check they hold the same value),
    Filter errors,
    Standardise Date format,
    Sort by subject and date.

    - Inputs: raw_data.csv, list of subjects, list of dates
    - Outputs: clean_data.csv, duplicates_info.csv

5. **data_checks.py**
Run checks on the final clean data, including:

    Number of data items as expected
    All subject-date combinations included
    Min/Max values

    - Inputs: clean_data.csv, Names of subjects to include, Names of dates to include
    - Outputs: Print any identified error
   
