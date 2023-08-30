import cv2
import easyocr
import csv
import os
from math import floor

def format_text(text):
    # Ensure text has 6 characters and consits of digits or decimal point
    formatted_text = ''.join(char for char in text if char.isdigit() or char == '.')
    formatted_text = formatted_text[:5]
    return formatted_text

# Input filenames for videos and CSV file
input_video_file1 = input("Enter the VOLTAGE input video filename: ")
input_video_file2 = input("Enter the CURRENT input video filename: ")
output_csv_file = input("Enter the output CSV filename: ")

# Use the current directory as the base directory
base_directory = os.getcwd()

# Construct full paths for input videos and output CSV
input_video_path1 = os.path.join(base_directory, input_video_file1)
input_video_path2 = os.path.join(base_directory, input_video_file2)
output_csv_path = os.path.join(base_directory, output_csv_file)

print(input_video_path1)
print(input_video_path2)
print(output_csv_path)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Open the video captures
video_capture1 = cv2.VideoCapture(input_video_path1)
video_capture2 = cv2.VideoCapture(input_video_path2)
frameRate = video_capture1.get(5)

# Create the CSV file if it doesn't exist
if not os.path.exists(output_csv_path):
    with open(output_csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'Voltage', 'Current'])

# Open the CSV file for writing (append mode)
csv_file = open(output_csv_path, 'a', newline='')
csv_writer = csv.writer(csv_file)

num_seconds = 0
try:
    while video_capture1.isOpened() and video_capture2.isOpened():
        ret1, frame1 = video_capture1.read()
        ret2, frame2 = video_capture2.read()

        if not ret1 or not ret2:
            break
        
        # Only one frame for each second is taken
        frameID = video_capture1.get(1)
        if (frameID % floor(frameRate) != 0):
            continue

        # Perform OCR on the frames
        results1 = reader.readtext(frame1)
        results2 = reader.readtext(frame2)

        value1 = None
        value2 = None

        # Find the number values with tens digit, ones digit, and 4 decimal places
        for (bbox, text, prob) in results1:
            value1 = format_text(text)

        for (bbox, text, prob) in results2:
            value2 = format_text(text)
 
        # Write to CSV if both values are found
        if value1 is not None and value2 is not None:
            print("Time:",num_seconds,"Voltage:", value1,"Current:", value2)
            csv_writer.writerow([num_seconds, value1, value2])

        num_seconds += 1

finally:
    # Close the CSV file
    csv_file.close()

    # Release the video captures
    video_capture1.release()
    video_capture2.release()
