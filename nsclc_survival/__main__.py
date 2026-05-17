#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __version__ import __version__
from preprocessing import RadiomicsPreprocessor
from feature_extractor import FeatureExtractor
from settings import ORGANIZED_DATA_PATH, PREPROCESSED_DATA_PATH, RADIOMICS_CONFIG_PATH, FEATURES_CSV_PATH

def main (): 
    print(__version__) 
    
    print("\n" + "#"*50)
    print(" 1. RUNNING RADIOMICS PREPROCESSING ".center(50, "#"))
    print("#"*50)

    processor = RadiomicsPreprocessor(
        organized_path=ORGANIZED_DATA_PATH, 
        preprocessed_path=PREPROCESSED_DATA_PATH
    )    

    processor.process_all_patients()
    
    print("\n" + "#" * 50)
    print(" 2. RUNNING FEATURE EXTRACTION  ".center(50, "#"))
    print("#" * 50)

    fe = FeatureExtractor(
        preprocessed_path=PREPROCESSED_DATA_PATH, 
        config_path=RADIOMICS_CONFIG_PATH 
    )
    
    fe.extract_all_features(output_csv=FEATURES_CSV_PATH)

if __name__ == "__main__":
    main()



