import os
import pandas as pd

# Limit of number of NaN values Pandas will interpolate consecutively 
NAN_VALUES_LIMIT = 2        
INPUT_DIRECTORY = r"E:\Downloads\Energy OCR Reader\Output_CSV"
OUTPUT_DIRECTORY = r"E:\Downloads\Energy OCR Reader\UPDATED_CSV"

for input_filename in os.listdir(INPUT_DIRECTORY): 
    if input_filename.endswith(".csv"):
        input_file_path = os.path.join(INPUT_DIRECTORY, input_filename)
        output_filename = input_filename[:-4] + '_updated.csv'
        output_file_path = os.path.join(OUTPUT_DIRECTORY, output_filename)
        
        df = pd.read_csv(input_file_path)
        df.interpolate(method='linear',limit_direction='forward',limit=NAN_VALUES_LIMIT,inplace=True)
        df.to_csv(output_file_path, index=False)
        print("Updated:",input_filename)

print("All files updated")

