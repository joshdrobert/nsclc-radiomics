from __future__ import annotations

from pathlib import Path
import urllib.request


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    url = "https://raw.githubusercontent.com/dannyjanani/Lung-Cancer-Detection/master/Lung1.clinical.csv"
    dest = PROJECT_ROOT / "data_raw" / "clinical_outcomes" / "Lung1.clinical.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "OpenSpecialtyRiskAtlas/0.1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        dest.write_bytes(response.read())
    (dest.parent / "SOURCE.txt").write_text(
        "Downloaded from a public GitHub mirror of Lung1.clinical.csv. Verify against the official TCIA/NSCLC-Radiomics attachment before submission.\n"
        f"URL: {url}\n",
        encoding="utf-8",
    )
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()

