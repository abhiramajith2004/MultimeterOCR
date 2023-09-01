import cv2
import easyocr
import csv
import os
from math import ceil

def format_text_float(text):
    formatted_text = ''.join(char for char in text if char.isdigit() or char == '.')
    formatted_text = formatted_text[:6]
    
    return float(formatted_text)

def format_text_voltage(text):
    val = format_text_float(text)
    
    while val > 10:     # since Voltage < 10
        val = val/10
        
    val = round(val, 3)
    return val

def format_text_current(text):
    val = format_text_float(text)
    
    while val > 2:         # since Current < 2
        val = val/10
        
    val = round(val, 4)
    return val

# Input filenames for videos and CSV file
input_video_file1 = input("Enter the VOLTAGE input video filename: ")
input_video_file2 = input("Enter the CURRENT input video filename: ") 
output_csv_file = input_video_file1[:-5] + '.csv'
input_video_file1 = input_video_file1 + '.mp4'
input_video_file2 = input_video_file2 + '.mp4'

# Use the current directory as the base directory
base_directory = os.getcwd()
videos_directory = os.path.join(base_directory, "Videos")
csv_directory = os.path.join(base_directory, "Output_CSV")

# Construct full paths for input videos and output CSV
input_video_path1 = os.path.join(videos_directory, input_video_file1)
input_video_path2 = os.path.join(videos_directory, input_video_file2)
output_csv_path = os.path.join(csv_directory, output_csv_file)

print(input_video_path1)
print(input_video_path2)
print(output_csv_path)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Open the video captures
video_capture1 = cv2.VideoCapture(input_video_path1)
video_capture2 = cv2.VideoCapture(input_video_path2)
frameRate = ceil(video_capture1.get(5))
print("Frame Rate:",frameRate)
    
# Create the CSV file for writing (write mode)
csv_file = open(output_csv_path, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Voltage', 'Current', 'Power'])

num_seconds = -1
try:
    while video_capture1.isOpened() and video_capture2.isOpened():
        ret1, frame1 = video_capture1.read()
        ret2, frame2 = video_capture2.read()

        if not ret1 or not ret2:
            break
        # Get one frame for each second
        frameID = video_capture1.get(1)
        if (frameID % frameRate != 0):
            continue
        num_seconds += 1

        # Perform OCR on the frames
        results1 = reader.readtext(frame1)
        results2 = reader.readtext(frame2)

        voltage = None
        current = None
        power = None

        # Find the number values with tens digit, ones digit, and 4 decimal places
        for (bbox, text, prob) in results1:
            voltage = format_text_voltage(text)

        for (bbox, text, prob) in results2:
            current = format_text_current(text)
            
        # Write to CSV if both values are found
        if voltage is not None and current is not None:
            power = round(voltage*current, 4)
            print("Time:",num_seconds,"Voltage:", voltage,"Current:", current, "Power:",power)
            csv_writer.writerow([num_seconds, voltage, current, power])
        else:
            print("Time:",num_seconds,"Voltage: None Current: None Power: None")
            csv_writer.writerow([num_seconds])

finally:
    # Close the CSV file
    print('Results saved at:', output_csv_path)
    csv_file.close()

    # Release the video captures
    video_capture1.release()
    video_capture2.release()
