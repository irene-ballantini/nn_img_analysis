from pathlib import Path

# --- Base Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# --- Subdirectories ---
RAW_DATA_PATH = DATA_DIR / "raw_data"
ORGANIZED_DATA_PATH = DATA_DIR / "organized_data"
PREPROCESSED_DATA_PATH = DATA_DIR / "preprocessed_data"

# --- Extracted Features output path ---
FEATURES_CSV_PATH = DATA_DIR / "features" / "extracted_features.csv"

# --- Config Paths ---
# Centralize the path to the radiomics config file
RADIOMICS_CONFIG_PATH = BASE_DIR / "configs" / "radiomics_config.yaml"

# --- Download Parameters ---
COLLECTION_NAME = "NSCLC-Radiomics"
N_PATIENTS = 100