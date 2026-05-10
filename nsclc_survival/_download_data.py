#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Download script for NSCLC-Radiomics dataset from TCIA. 

This script connects to the TCIA API, retrieves metadata for the NSCLC-Radiomics collection, 
filters for patients with both CT and RTSTRUCT modalities,
and downloads the DICOM series for a subset of patients into a specified directory.

"""

from tcia_utils import nbia
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / "data" / "raw_data"

# Creation of folder for raw data
data_path.mkdir(parents=True, exist_ok=True)

# 1. Metadata retrieval
print("Connecting to TCIA... Retrieving series list.")
df = nbia.getSeries(collection="NSCLC-Radiomics", format="df")

#print(df.columns)
#print(df.info())

# 2. Filtering logic: we are looking for patients with CT + RTSTRUCT
patients_ct = set(df[df['Modality'] == 'CT']['PatientID'])
patients_rt = set(df[df['Modality'] == 'RTSTRUCT']['PatientID'])
valid_patients = sorted(list(patients_ct.intersection(patients_rt)))

print(f"Found {len(valid_patients)} complete patients.")

# 3. Select a subset (e.g. 60)
n_patients = 60
subset_patients = valid_patients[:n_patients]
df_to_download = df[df['PatientID'].isin(subset_patients)]

series_dict_list = df_to_download.to_dict(orient='records')

print(f"Starting download for {n_patients} patients in {data_path}...")
nbia.downloadSeries(series_dict_list, path=data_path)
print("Download completed successfully!")

