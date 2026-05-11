#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
To convert clinical data in format NIfTI (.nii.gz).

To summarize:

- rt_utils trasforms the vectors (points of the contours) in an array (pixels).

- SimpleITK trasforms the array (pixels) in a spatial volume (voxels) ready to be saved as a .nii.gz file.
"""

import numpy as np
import SimpleITK as sitk
from pathlib import Path
from rt_utils import RTStructBuilder
from settings import ORGANIZED_DATA_PATH, PREPROCESSED_DATA_PATH

def numpy_to_itk(mask_np, reference_image):
    # rt_utils returns (H, W, Slices), SimpleITK works with (Slices, H, W) 
    # or it requires a reordering. rt_utils is already aligned with the DICOM series.
    mask_itk = sitk.GetImageFromArray(mask_np.astype(np.uint8).transpose(2, 0, 1))
    
    # Copy spatial metadata from the original CT
    mask_itk.SetSpacing(reference_image.GetSpacing())
    mask_itk.SetOrigin(reference_image.GetOrigin())
    mask_itk.SetDirection(reference_image.GetDirection())
    return mask_itk

PREPROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

# Retrieve patient folders in the organized data direcotry
patient_folders = sorted([f for f in ORGANIZED_DATA_PATH.iterdir() if f.is_dir()])
print(f"Found {len(patient_folders)} patients to process.")

for i, patient_dir in enumerate(patient_folders, start=1):
    patient_id = patient_dir.name
    print(f"\nProcessing folder {i}/{len(patient_folders)}: Patient {patient_id}")
        
    path_ct = patient_dir / "CT"
    #Note: RTSTRUCT file usually has a single file
    rt_files = list((patient_dir / "RTSTRUCT").glob("*.dcm")) 

    if not rt_files:
        print(f"Skipping {patient_id}: No file RTSTRUCT found.")
        continue

    path_rtstruct = rt_files[0]  # Take the first RTSTRUCT file found

    print(f"CT Path: {path_ct}")
    print(f"RT Path: {path_rtstruct}")

    try:
        rtstruct = RTStructBuilder.create_from(
            dicom_series_path=str(path_ct), 
            rt_struct_path=str(path_rtstruct),
        )

        rois = rtstruct.get_roi_names()
        print(f"ROI found for this patient {patient_id}: {rois}")

        if not rois:
            print("WARNING: No ROI loaded correctly.")
        
        # GTV-1 = label for Primary Gross Tumor Volume
        roi_target = "GTV-1" 

        if roi_target not in rois:
            print(f"Skipping {patient_id}: ROI '{roi_target}' not found. Available ROIs: {rois}")
            continue
        
        # Extract the tumor mask 
        tumor_mask = rtstruct.get_roi_mask_by_name(roi_target)  

        # Verify the dimensions of the mask
        print(f"Shape of the mask: {tumor_mask.shape}") 
        # Should be (height, width, number_of_slices)
        
        # Load the CT series as a SimpleITK image
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(str(path_ct))
        reader.SetFileNames(dicom_names)
        ct_image = reader.Execute()

        # Now the object ct_image "knows" the size of the voxels (e.g., 1mm x 1mm x 3mm)

        tumor_mask_itk = numpy_to_itk(tumor_mask, ct_image)
        
        # Saving in NIfTI format
        output_patient_dir = PREPROCESSED_DATA_PATH / patient_id
        output_patient_dir.mkdir(parents=True, exist_ok=True)

        sitk.WriteImage(ct_image, str(output_patient_dir / "image.nii.gz"))
        sitk.WriteImage(tumor_mask_itk, str(output_patient_dir / "label.nii.gz"))

        print(f"Completed: {patient_id} (CT + Mask saved)")

    except Exception as e:
        print(f"Skipping patient {patient_id} due to RTSTRUCT error: {e}")
    continue

print(f"\nPreprocessing completed! The NIfTI files are in: {PREPROCESSED_DATA_PATH}")
