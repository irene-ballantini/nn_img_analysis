#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Download script for NSCLC-Radiomics dataset from TCIA. 

This script connects to the TCIA API, retrieves metadata for the NSCLC-Radiomics collection, 
filters for patients with both CT and RTSTRUCT modalities,
and downloads the DICOM series for a subset of patients into a specified directory.

Attributes (from settings.py):
    RAW_DATA_PATH (Path): Directory where raw DICOM data will be saved.
    COLLECTION_NAME (str): Name of the TCIA collection to download.
    N_PATIENTS (int): Number of valid patients to retrieve.

"""

from tcia_utils import nbia
from settings import RAW_DATA_PATH, COLLECTION_NAME, N_PATIENTS

# Creation of folder for raw data
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

# 1. Metadata retrieval
print("Connecting to TCIA... Retrieving series list.")
df = nbia.getSeries(collection=COLLECTION_NAME, format="df")

#print(df.columns)
#print(df.info())

# 2. Filtering logic: we are looking for patients with CT + RTSTRUCT
patients_ct = set(df[df['Modality'] == 'CT']['PatientID'])
patients_rt = set(df[df['Modality'] == 'RTSTRUCT']['PatientID'])
valid_patients = sorted(list(patients_ct.intersection(patients_rt)))

print(f"Found {len(valid_patients)} complete patients.")

# 3. Select a subset (e.g. 100)
subset_patients = valid_patients[:N_PATIENTS]
df_to_download = df[df['PatientID'].isin(subset_patients)]

series_dict_list = df_to_download.to_dict(orient='records')

print(f"Starting download for {N_PATIENTS} patients in {RAW_DATA_PATH}...")
nbia.downloadSeries(series_dict_list, path=RAW_DATA_PATH)
print("Download completed successfully!")

