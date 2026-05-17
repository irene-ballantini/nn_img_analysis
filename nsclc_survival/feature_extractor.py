#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import time
import pandas as pd
from radiomics import featureextractor

class FeatureExtractor:
    def __init__(self, preprocessed_path, config_path):

        self.preprocessed_path = Path(preprocessed_path)
        self.config_path = Path(config_path)

        if self.config_path.exists():
            self.extractor = featureextractor.RadiomicsFeatureExtractor(str(self.config_path))
        else:
            print(f"[WARNING] Config file not found in {self.config_path}. Using default settings.")
            self.extractor = featureextractor.RadiomicsFeatureExtractor()
        
        print("Image types enabled:", self.extractor.enabledImagetypes)
        print("Feature classes enabled:", self.extractor.enabledFeatures)

    def extract_all_features(self, output_csv):
        patient_folders = sorted([f for f in self.preprocessed_path.iterdir() if f.is_dir()])
        print(f"Found {len(patient_folders)} patients.")
        
        start_total_time = time.time()    # Start total timer
        rows = []
        for p in patient_folders:
            image_path = p / "image.nii.gz"
            mask_path = p / "label.nii.gz"
            patient_id = p.name

            if not image_path.exists() or not mask_path.exists():
                print(f"[SKIP] {patient_id}: image or mask missing")
                continue

            print(f"Feature extraction for {patient_id}...")
            start_patient_time = time.time()  # Start timer for this patient
            
            try:
                feats = self.extract_radiomics(image_path, mask_path, patient_id)
                rows.append(feats)
                
                # Calculate duration time for this patient 
                patient_duration = time.time() - start_patient_time
                print(f"--> Done in {patient_duration:.2f} seconds.")

            except Exception as e:
                print(f"[ERROR] {patient_id}: {e}")
                continue

        if not rows:
            print("No features extracted.")
            return
        
        # DataFrame creation
        df = pd.DataFrame(rows)
        # PatientID as first column
        cols = ["PatientID"] + [c for c in df.columns if c != "PatientID"]
        df = df[cols]
        
        output_csv = Path(output_csv)
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_csv, index=False)
        
        # Calculate total duration time
        total_duration = time.time() - start_total_time
        hours = int(total_duration // 3600)
        minutes = int((total_duration % 3600) // 60)
        seconds = total_duration % 60

        print(f"\nExtraction completed. File saved in {output_csv}")
        print(f"Number of processed patients: {len(rows)}")
        print(f"Number of radiomics features (columns): {df.shape[1] - 1}")

        if hours > 0:
            time_str = f"{hours}h {minutes}m {seconds:.2f}s"
        else:
            time_str = f"{minutes}m {seconds:.2f}s"
            
        print(f"Total execution time: {time_str} (Average: {total_duration/len(rows):.2f}s per patient)")

    def extract_radiomics(self, image_path, mask_path, patient_id):
        result = self.extractor.execute(str(image_path), str(mask_path))
        
        # Remove metadata diagnostics
        clean = {}
        for k, v in result.items():
            if k.startswith("diagnostics_"):
                continue
            clean[k] = v

        clean["PatientID"] = patient_id
        return clean
