#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd

def save_features_to_csv(features_list, output_path):
    """
    Converts a list of dictionaries to a Pandas DataFrame and saves it as a CSV file.
    Args:
        features_list (list of dict): List where each element is a dictionary of features for a single patient.
        output_path (str or Path): Path to save the CSV file.
    """
    if not features_list:
        print("[WARNING] No features to save.")
        return

    # DataFrame creation
    df = pd.DataFrame(features_list)
    
    # PatientID as first column
    cols = ["PatientID"] + [c for c in df.columns if c != "PatientID"]
    df = df[cols]
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Saving
    df.to_csv(output_path, index=False)
    print(f"[INFO] File saved successfully in: {output_path}")
    print(f"[INFO] Total columns written: {df.shape[1]} (PatientID + {df.shape[1] - 1} features)")