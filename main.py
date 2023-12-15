import subprocess
import xml.etree.ElementTree as ET
import os
import shutil

def print_xmp_rating(file_path):
    # Run the ExifTool command with the -b option to extract binary data
    process = subprocess.Popen(['exiftool', '-XMP', '-b', file_path],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print("Error:", err.decode())
        return

    # Parse the XML output
    try:
        root = ET.fromstring(out)
        namespaces = {'xmp': 'http://ns.adobe.com/xap/1.0/'}  # Define the namespace
        rating = root.find('.//xmp:Rating', namespaces)

        if rating is not None:
            return(f"Rating: {rating.text}")
        else:
            return("Rating not found")
    except ET.ParseError as e:
        return("Error parsing XML:", e)
 
# assign directory
input_directory = '/Volumes/VIRAL 256/DCIM/107MSDCF'
output_directory = 'output'
 
# iterate over files in 
# that directory
for filename in os.scandir(input_directory):
    if filename.is_file():
        data = print_xmp_rating(filename)
        if data == 'Rating: 5':
            shutil.copy(filename, output_directory)
