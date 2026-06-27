from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parents[0]
sys.path.append(str(REPO_ROOT / "_shared" / "02_common_functions"))

from survival_models import fit_cox_model, write_km_plot  # noqa: E402


def main() -> None:
    data = pd.read_csv(PROJECT_ROOT / "data_processed" / "nsclc_radiomics_clinical_survival_cohort.csv")
    predictors = ["age", "clinical.T.Stage", "Clinical.N.Stage", "Clinical.M.Stage", "Overall.Stage", "Histology", "gender", "series_n", "total_image_count"]
    
    radiomics_file = PROJECT_ROOT / "data_processed" / "radiomics_features.csv"
    if radiomics_file.exists():
        radiomics_df = pd.read_csv(radiomics_file)
        data = data.merge(radiomics_df, on="PatientId", how="inner")
        radiomics_cols = [col for col in radiomics_df.columns if col.startswith("original_")]
        predictors.extend(radiomics_cols)
        print(f"Integrated {len(radiomics_cols)} PyRadiomics features into the Cox model!")

    fit_cox_model(data, predictors, "survival_time_days", "event_death", PROJECT_ROOT / "tables", "nsclc")
    write_km_plot(data, "survival_time_days", "event_death", "Overall.Stage", PROJECT_ROOT / "figures" / "nsclc_km_by_stage.png")
    print("Wrote NSCLC Cox survival model")


if __name__ == "__main__":
    main()

