# An Open-Source CT Radiomics-Clinical Risk Score for Survival Prediction in Non-Small Cell Lung Cancer

## Abstract

### Background
Pretreatment CT imaging may support interpretable risk stratification in non-small cell lung cancer, but radiomics pipelines require careful inventory of imaging series, segmentation masks, and linked outcomes.

### Objective
To develop an open-source workflow for a CT radiomics-clinical NSCLC risk score using NSCLC-Radiomics from The Cancer Imaging Archive.

### Methods
The current reproducible first pass uses TCIA public patient and series metadata to construct an imaging inventory. Subsequent analyses will add DICOM images, segmentation masks, radiomics features, and clinical survival outcomes.

### Results
The available metadata inventory includes 422 patients and 1,265 imaging series. Manuscript-ready inventory and missingness tables are generated in `tables/`.

### Conclusions
The project is ready for full radiomics feature extraction once DICOM imaging, masks, and outcome files are downloaded through TCIA/NBIA workflows.

## Introduction

## Methods

### Data Source
NSCLC-Radiomics is accessed through TCIA. Public metadata were downloaded through TCIA/NBIA APIs; raw DICOM images are not redistributed.

### Current Analytic Dataset
The current dataset is an imaging inventory containing patient IDs, sex, modality, manufacturer, image counts, and file-size summaries.

### Planned Radiomics Workflow
DICOM images will be loaded, resampled, normalized, paired with tumor masks, and processed with PyRadiomics. Candidate features will be combined with clinical variables for survival modeling.

## Results

Metadata tables are available in `tables/`. Survival modeling is not yet performed because clinical outcome files and image-derived features have not yet been incorporated.

## Discussion

This first pass establishes data readiness rather than a final risk model.

## Limitations

No radiomics features, tumor masks, or survival outcomes are included yet.

## Conclusion

The project now has a reproducible metadata inventory and is ready for TCIA bulk image and outcome ingestion.

