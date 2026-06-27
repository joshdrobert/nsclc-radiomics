from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT
sys.path.append(str(REPO_ROOT / "_shared" / "02_common_functions"))

from validation_extras import simple_km_table  # noqa: E402


def main() -> None:
    data = pd.read_csv(PROJECT_ROOT / "data_processed" / "nsclc_radiomics_clinical_survival_cohort.csv")
    simple_km_table(data, "survival_time_days", "event_death", "Overall.Stage", PROJECT_ROOT / "tables" / "table_survival_by_stage_horizon.csv")
    print("Wrote NSCLC survival horizon summary")


if __name__ == "__main__":
    main()

