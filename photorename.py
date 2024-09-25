#!/usr/bin/env python3

"""
A script to rename photo files using EXIF data OR today's date

# G. Wilburn, 2024
"""
# $Id: photorename.py,v 1.2 2024/09/24 18:20:16 gene Exp gene $

import sys
import re
import os
import platform
from datetime import date
from PIL import Image
from PIL.ExifTags import TAGS
#import exifread

# Get and process optional command line args
numargs = len(sys.argv) - 1  # Subtract 1 to exclude the script name
if numargs > 0:
    for arg in sys.argv[1:]:  # Start from index 1 to skip the script name
        if sys.argv[1]:
            photog = sys.argv[1]
        if sys.argv[2]:
            tagstr = sys.argv[2]

# If no optional args have been sent then set these values
if 'photog' not in globals():
    photog = "g"
if 'tagstr' not in globals():
    tagstr = "tags"

filename_pairs = []

# Get today's date in yyyymmdd format
today = date.today().strftime("%Y%m%d")

##### TARGET DIRECTORIES #####
# Set path to target directory containing files to be renamed
linux_targetdir = "/home/gene/Dropbox/Images/tmp/"
mac_targetdir = "/Users/gene/Dropbox/Images/tmp/"
win_targetdir = "C:/Users/gene/Dropbox/Images/tmp/"

os_name = platform.system()
if os_name == "Windows":
    targetdir = win_targetdir
elif os_name == "Darwin":
    targetdir = mac_targetdir
elif os_name == "Linux":
    targetdir = linux_targetdir
else:
    print("System platform not recognized")
    sys.exit()

print(targetdir)


# Open target directory and read in the filenames
# files = os.listdir(targetdir)
files = [f for f in os.listdir(targetdir) if not f.startswith('.')]

# Process files sequentially
for filename in files:
    # Check if it's a file (not a subdirectory)
    if os.path.isfile(os.path.join(targetdir, filename)):
        # Construct full file path
        file_path = os.path.join(targetdir, filename)
        base, ext = os.path.splitext(filename)
    else:
        continue

    # Extract EXIF data
    # Open the image file
    date_to_use = today
    image = Image.open(file_path)
    exif_data = image.getexif()

    if exif_data:
    # Find the DateTimeOriginal tag
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == 'DateTime':
                date_taken = value
                date_to_use = date_taken.split()[0].replace(':', '')
    else:
        # If DateTimeOriginal not found, use today's date
        date_to_use = today

    # Construct new filename
    file_extension = os.path.splitext(filename)[1]
    file_extension = file_extension.lower().strip()
    if file_extension in ("jpeg", ".jpeg"):
           file_extension = ".jpg"

    # Add filename pairs to the list
    new_filename = f"{date_to_use}-xxx{photog}--{tagstr}{file_extension}"
    filename_pairs.append((new_filename, filename))


# Sort the list based on the new filename
filename_pairs.sort(key=lambda x: x[0])

# Set some variables to be used in assigning sequence number (seqnum) in a given day
prev_file = ""
pattern = r'xxx'

for new_filename, old_filename in filename_pairs:
 	# Check to see if seqnum needs incrementing or resetting
    if new_filename[:8] == prev_file:
        seqnum += 1
    else:
        prev_file = new_filename[:8]
        seqnum = 1
    # Use a regular expression to replace 'xxx' with an actual sequence number
    final_filename = re.sub(pattern, "{seqnum:03d}", new_filename)
    final_filename = f"{new_filename[:8]}-{seqnum:03d}{photog}--{new_filename[15:]}"
    # refresh path/file names    
    new_file_path = os.path.join(targetdir, final_filename)
    old_file_path = os.path.join(targetdir, old_filename)
    # Finally, rename the file
    os.rename(old_file_path, new_file_path)    
    print(f"Renamed: {old_filename} -> {final_filename}")  

print("File renaming completed.")

# Goodbye

