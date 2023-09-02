import cv2
import easyocr
import csv
import os
from math import ceil

# Directories for videos and CSV file
VIDEO_DIRECTORY = r"E:\Downloads\Energy OCR Reader\Videos"
CSV_DIRECTORY = r"E:\Downloads\Energy OCR Reader\Output_CSV"

print("Input directory:",VIDEO_DIRECTORY)
print("Output directory:",CSV_DIRECTORY)

# List of videos already processed
already_processed_vids = []

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

def format_text_power(text):
    formatted_text = ''.join(char for char in text if char.isdigit() or char == '.')
    formatted_text = formatted_text[:6]
    
    val = float(formatted_text)
    while val > 10:     # since Power < 10
        val = val/10
        
    val = round(val, 3)
    return val

def extract_values_toCSV(input_video_name):
    
    input_video_path = os.path.join(VIDEO_DIRECTORY, input_video_name)
    # remove .mp4 extension
    output_csv_name = input_video_name[:-4] + '.csv'       
    output_csv_path = os.path.join(CSV_DIRECTORY, output_csv_name)
    
    # Output CSV file exists
    if os.path.exists(output_csv_path):
        print(f"Output CSV for {input_video_name} already exists")
        already_processed_vids.append(input_video_name)
        return 1
    
    # Open the video captures
    video_capture = cv2.VideoCapture(input_video_path)
    frameRate = ceil(video_capture.get(5))
    print("Video:", input_video_name)
    print("Frame Rate:",frameRate)
    
    # Create the CSV file for writing (write mode)
    csv_file = open(output_csv_path, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Timestamp', 'Power'])

    num_seconds = -1
    try:
        while video_capture.isOpened():
            ret1, frame1 = video_capture.read()

            if not ret1:
                break
            
            # Get one frame for each second
            frameID = video_capture.get(1)
            if (frameID % frameRate != 0):
                continue
            num_seconds += 1

            # Perform OCR on the frames
            results1 = reader.readtext(frame1)
            power = None

            # Find the number value
            for (bbox, text, prob) in results1:
                power = format_text_power(text)

            # Write to CSV if value is found
            if power is not None:
                print("Time:",num_seconds,"Power:",power)
                csv_writer.writerow([num_seconds, power])
            else:
                print("Time:",num_seconds,"Power: None")
                csv_writer.writerow([num_seconds])

    finally:
        # Close the CSV file
        print('Results saved to:', output_csv_path)
        csv_file.close()

        # Release the video captures
        video_capture.release()
        return 0

# Main
num_videos_found = 0
for video_filename in os.listdir(VIDEO_DIRECTORY): 
    if video_filename.endswith(".mp4"):
        num_videos_found += 1
        extract_values_toCSV(video_filename)
        
num_videos_processed = num_videos_found - len(already_processed_vids)
print(f"Number of videos Found : {num_videos_found} Processed: {num_videos_processed}")
if num_videos_found != num_videos_processed:
    print("List of videos already processed:", already_processed_vids)
        