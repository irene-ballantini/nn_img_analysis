#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DICOM data organization utility.

This script parses DICOM files within the raw data directory, retrieves 
metadata (PatientID and Modality) using pydicom, and moves the files into 
a new structured directory format organized by PatientID and Modality:
../data/organized_data/{PatientID}/{Modality}/

"""

import shutil
import pydicom
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
raw_data_path = BASE_DIR / "data" / "raw_data"
organized_data_path = BASE_DIR / "data" / "organized_data"

organized_data_path.mkdir(parents=True, exist_ok=True)

# Check whether the raw data folder exists or has already been removed (e.g. if the script is run twice)
if not raw_data_path.exists():
    print(f"raw folder not found: probably all files have already been moved and the raw folder removed.")
    exit()

all_folders = [f for f in raw_data_path.iterdir() if f.is_dir()]

print(f"Analysing {len(all_folders)} folders in progress...")

if len(all_folders) == 0:
    print("All folders have already been moved!")
else:
    # Reorganization cycle
    for folder_path in all_folders:
    
        # Find .dcm files in the folder
        files = list(folder_path.glob("*.dcm"))    
        if files:
            try:
                # Read the first file to get metadata
                sample_dcm = pydicom.dcmread(files[0])

                patient_id = sample_dcm.PatientID
                modality = sample_dcm.Modality
                # series_uid = sample_dcm.SeriesInstanceUID

                # Create new folder name
                target_dir = organized_data_path / patient_id / modality
                target_dir.mkdir(parents=True, exist_ok=True)

                # Move files to the new location
                for f in files:
                    shutil.move(str(f), str(target_dir / f.name))

                print(f"Moved: {patient_id} - {modality}")

            except Exception as e:
                print(f"Error processing {folder_path}: {e}")
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