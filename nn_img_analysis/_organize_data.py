#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script organizes the downloaded DICOM files into a structured format based on patient ID and modality.

import os
import shutil
import pydicom

raw_data_path = "../data/raw_data"
organized_data_path = "../data/organized_data"

os.makedirs(organized_data_path, exist_ok=True)

# Check whether the raw data folder exists or has already been removed (e.g. if the script is run twice)
if not os.path.exists(raw_data_path):
    print("raw folder not found!")
    exit()

all_folders = os.listdir(raw_data_path)

print(f"Analysing {len(os.listdir(raw_data_path))} folders in progress...")

if len(all_folders) == 0:
    print("All folders have already been moved!")
else:
    # Reorganization cycle
    for folder_name in os.listdir(raw_data_path):
        folder_path = os.path.join(raw_data_path, folder_name)
    
        if not os.path.isdir(folder_path):
            continue
    
        # Find .dcm files in the folder
        files = [f for f in os.listdir(folder_path) if f.endswith('.dcm')]
    
        if files:
            try:
                # Read the first file to get metadata
                sample_dcm = pydicom.dcmread(os.path.join(folder_path, files[0]))

                patient_id = sample_dcm.PatientID
                modality = sample_dcm.Modality
                series_uid = sample_dcm.SeriesInstanceUID

                # Create new folder name
                target_dir = os.path.join(organized_data_path, patient_id, modality)
                os.makedirs(target_dir, exist_ok=True)

                # Move files to the new location
                for f in files:
                    shutil.move(os.path.join(folder_path, f), os.path.join(target_dir, f))

                print(f"Moved: {patient_id} - {modality}")

            except Exception as e:
                print(f"Error processing {folder_name}: {e}")
                continue # if there's an error, don't delete the folder

        # Remove the original folder
        shutil.rmtree(folder_path)

    # Now remove also the raw folder
    try:
        shutil.rmtree(raw_data_path)
        print(f"\nSuccessfully removed the entire '{raw_data_path}' folder.")
    except Exception as e:
        print(f"Could not remove folder {raw_data_path}: {e}")
        

    print("\nDone! Now all data are organized in '../data/organized' folder divided per patient")