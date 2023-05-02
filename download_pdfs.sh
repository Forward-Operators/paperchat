#!/bin/sh

output_folder="pdf"

# Create output folder if it doesn't exist
mkdir -p "$output_folder"

# Read the gs_paths.txt file line by line and download the PDF files
while IFS= read -r gs_path; do
    gsutil cp "$gs_path" "$output_folder/"
done < gs_paths_part.txt
