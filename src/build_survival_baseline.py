from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parents[0]
sys.path.append(str(REPO_ROOT / "_shared" / "02_common_functions"))

from tabular_risk_model import train_logistic_score  # noqa: E402


def main() -> None:
    inventory = pd.read_csv(PROJECT_ROOT / "data_processed" / "nsclc_radiomics_imaging_inventory.csv")
    clinical = pd.read_csv(PROJECT_ROOT / "data_raw" / "clinical_outcomes" / "Lung1.clinical.csv")
    clinical = clinical.rename(columns={"PatientID": "PatientId", "Survival.time": "survival_time_days", "deadstatus.event": "event_death"})
    cohort = inventory.merge(clinical, on="PatientId", how="inner")
    cohort["outcome_2yr_mortality"] = ((cohort["event_death"].eq(1)) & (pd.to_numeric(cohort["survival_time_days"], errors="coerce") <= 730)).astype(int)
    out = PROJECT_ROOT / "data_processed" / "nsclc_radiomics_clinical_survival_cohort.csv"
    cohort.to_csv(out, index=False)
    predictors = ["age", "clinical.T.Stage", "Clinical.N.Stage", "Clinical.M.Stage", "Overall.Stage", "Histology", "gender", "series_n", "total_image_count"]
    
    radiomics_file = PROJECT_ROOT / "data_processed" / "radiomics_features.csv"
    if radiomics_file.exists():
        radiomics_df = pd.read_csv(radiomics_file)
        cohort = cohort.merge(radiomics_df, on="PatientId", how="inner")
        radiomics_cols = [col for col in radiomics_df.columns if col.startswith("original_")]
        predictors.extend(radiomics_cols)
        print(f"Integrated {len(radiomics_cols)} PyRadiomics features into the baseline cohort!")

    train_logistic_score(cohort, [p for p in predictors if p in cohort.columns], "outcome_2yr_mortality", PROJECT_ROOT / "models", PROJECT_ROOT / "tables")
    cohort["outcome_2yr_mortality"].value_counts(dropna=False).rename_axis("outcome_2yr_mortality").reset_index(name="n").to_csv(
        PROJECT_ROOT / "tables" / "table_2yr_mortality_counts.csv", index=False
    )
    print(f"Wrote NSCLC survival baseline cohort: {len(cohort):,} patients")


if __name__ == "__main__":
    main()

