from __future__ import annotations

import os
import sys
import logging
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parents[0]

# Set up logging to avoid clutter
logging.getLogger("radiomics").setLevel(logging.WARNING)

def get_pyradiomics_extractor():
    try:
        from radiomics import featureextractor
        import SimpleITK as sitk
    except ImportError:
        print("PyRadiomics and/or SimpleITK are not installed.")
        print("Please install them in a Python 3.10/3.11 environment using:")
        print("  pip install pyradiomics SimpleITK")
        sys.exit(1)

    # Standard settings adhering to IBSI guidelines
    settings = {
        'binWidth': 25,
        'resampledPixelSpacing': [1.0, 1.0, 1.0],  # Isotropic resampling
        'interpolator': sitk.sitkBSpline,
        'normalize': True,
        'normalizeScale': 100,
    }
    
    extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
    extractor.enableAllFeatures()  # Enable first-order, shape, texture (GLCM, GLRLM, etc.)
    return extractor

def main() -> None:
    dicom_dir = PROJECT_ROOT / "data_raw" / "dicom"
    masks_dir = PROJECT_ROOT / "data_raw" / "masks"
    
    if not dicom_dir.exists() or not masks_dir.exists():
        print(f"Data directories not found at:")
        print(f"  {dicom_dir}")
        print(f"  {masks_dir}")
        print("\nPlease download the NSCLC-Radiomics CT images and segmentation masks from TCIA:")
        print("  https://www.cancerimagingarchive.net/collection/nsclc-radiomics/")
        print("Place DICOM files in 'data_raw/dicom/' and segmentation masks in 'data_raw/masks/'.")
        return

    patients = [d for d in os.listdir(dicom_dir) if os.path.isdir(dicom_dir / d)]
    if not patients:
        print(f"No patient folders found inside {dicom_dir}.")
        return

    print(f"Found {len(patients)} patient folders. Initializing PyRadiomics extractor...")
    extractor = get_pyradiomics_extractor()
    
    records = []
    
    for i, patient in enumerate(patients, 1):
        patient_dicom = dicom_dir / patient
        patient_mask = masks_dir / f"{patient}.nii.gz" # or matching naming convention
        
        if not patient_mask.exists():
            # Check for alternative mask names, e.g. .nii, RTSTRUCT
            alternative_masks = list(masks_dir.glob(f"{patient}*"))
            if alternative_masks:
                patient_mask = alternative_masks[0]
            else:
                print(f"[{i}/{len(patients)}] Skipping patient {patient}: Mask file not found.")
                continue

        print(f"[{i}/{len(patients)}] Extracting features for patient {patient}...")
        try:
            # SimpleITK reader parses the DICOM series
            reader = sitk.ImageSeriesReader()
            dicom_names = reader.GetGDCMSeriesFileNames(str(patient_dicom))
            reader.SetFileNames(dicom_names)
            image = reader.Execute()
            
            mask = sitk.ReadImage(str(patient_mask))
            
            # Extract features
            result = extractor.execute(image, mask)
            
            # Store patient features (prefixing PyRadiomics output)
            patient_record = {"PatientId": patient}
            for key, val in result.items():
                if key.startswith("original_"):
                    # PyRadiomics feature values can be float or numpy arrays (we pull the scalar value)
                    try:
                        patient_record[key] = float(val)
                    except (TypeError, ValueError):
                        patient_record[key] = str(val)
                        
            records.append(patient_record)
            
        except Exception as e:
            print(f"Error processing patient {patient}: {e}")
            continue

    if records:
        df = pd.DataFrame(records)
        out_path = PROJECT_ROOT / "data_processed" / "radiomics_features.csv"
        df.to_csv(out_path, index=False)
        print(f"\nRadiomics extraction complete! Extracted features for {len(records)} patients.")
        print(f"Wrote outputs to: {out_path}")
    else:
        print("\nNo features were extracted. Check folder structures and mask names.")

if __name__ == "__main__":
    main()
