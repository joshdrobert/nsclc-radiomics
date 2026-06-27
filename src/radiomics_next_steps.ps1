# Full radiomics extraction requires local DICOMs, tumor masks, and dependencies.
# Run after downloading DICOM/mask files from TCIA/NBIA into data_raw/dicom and data_raw/masks.

python -m pip install pyradiomics SimpleITK

# Then implement/execute a PyRadiomics feature extraction script against:
#   04_thoracic_nsclc_radiomics/data_raw/dicom/
#   04_thoracic_nsclc_radiomics/data_raw/masks/
#
# This file is intentionally a guarded next-step script, not a claim that radiomics
# features have already been extracted.

