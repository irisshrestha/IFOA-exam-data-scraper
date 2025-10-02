import os
import zipfile

zips_dir = "zips2"
pdf_dir = "pdfs2"
os.makedirs(pdf_dir, exist_ok=True)


for zip_file in os.listdir(zips_dir):
    with zipfile.ZipFile(f"{zips_dir}/{zip_file}", "r") as zip_ref:
        zip_ref.extractall(pdf_dir)
