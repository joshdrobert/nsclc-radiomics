from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT
sys.path.append(str(REPO_ROOT / "_shared" / "02_common_functions"))

from tcia_metadata import build_nsclc_metadata, write_nsclc_summary  # noqa: E402


def main() -> None:
    patient_csv = PROJECT_ROOT / "data_raw" / "tcia_metadata" / "getPatient.csv"
    series_csv = PROJECT_ROOT / "data_raw" / "tcia_metadata" / "getSeries.csv"
    processed = PROJECT_ROOT / "data_processed"
    tables = PROJECT_ROOT / "tables"
    processed.mkdir(parents=True, exist_ok=True)
    analysis = build_nsclc_metadata(patient_csv, series_csv)
    analysis.to_csv(processed / "nsclc_radiomics_imaging_inventory.csv", index=False)
    write_nsclc_summary(analysis, series_csv, tables)
    print(f"Wrote NSCLC-Radiomics imaging inventory: {len(analysis):,} patients")


if __name__ == "__main__":
    main()

