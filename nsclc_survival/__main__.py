#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __version__ import __version__
from preprocessing import RadiomicsPreprocessor
from settings import ORGANIZED_DATA_PATH, PREPROCESSED_DATA_PATH

def main (): 
    print(__version__) 

    processor = RadiomicsPreprocessor(ORGANIZED_DATA_PATH, PREPROCESSED_DATA_PATH)    

    processor.process_all_patients()

if __name__ == "__main__":
    main()



