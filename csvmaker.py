import os
import csv
from docx import Document

# Function to read the content of a .docx file


def read_docx_content(file_path):
    doc = Document(file_path)
    content = ''
    for paragraph in doc.paragraphs:
        content += paragraph.text + '\n'
    return content.strip()

# Function to iterate over files in a folder, read their content, and write to CSV


def create_csv_from_folder(folder_path, output_file):
    # Open the CSV file in write mode
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        # Define the headers for the CSV file
        fieldnames = ['Content', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the headers to the CSV file
        writer.writeheader()

        # Iterate over files in the folder
        for filename in os.listdir(folder_path):
            # Check if the file is a .docx file
            if filename.endswith('.docx'):
                # Read the content of the .docx file
                content = read_docx_content(
                    os.path.join(folder_path, filename))
                # Write the content and type to the CSV file
                writer.writerow({'Content': content, 'Type': 'Marketing&Sales'})


# Specify the input folder containing the .docx files
input_folder = 'StemmationProcessMarketing&Sales'

# Specify the output CSV file
output_csv = 'testCSV_M&S.csv'

# Call the function to create the CSV file from the folder
create_csv_from_folder(input_folder, output_csv)

print(f"CSV file '{output_csv}' created successfully.")
