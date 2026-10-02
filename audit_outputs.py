"""Create literal L1 review flags for a saved project run.

These checks only detect exact required/forbidden strings; they do not grade
meaning or replace the manual judgments in evaluation_results.csv.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from run_project import QUESTIONS


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=project_dir / "results" / "top_k_comparison_final_prompt_run.csv",
        help="saved model-output CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project_dir / "results" / "l1_heuristic_audit.csv",
        help="output CSV for literal review flags",
    )
    args = parser.parse_args()
    cases = {case["id"]: case for case in QUESTIONS}
    rows = []
    with args.input.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            case = cases[row["case_id"]]
            answer = row["answer"].casefold()
            missing = [term for term in case["required_terms"] if term.casefold() not in answer]
            forbidden = [claim for claim in case["forbidden_claims"] if claim.casefold() in answer]
            rows.append(
                {
                    "top_k": row["top_k"],
                    "case_id": row["case_id"],
                    "literal_required_terms_missing": "; ".join(missing),
                    "literal_forbidden_claims_found": "; ".join(forbidden),
                    "review_note": "Heuristic flags only; paraphrases may be false positives/negatives. See manual score.",
                }
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} heuristic review rows to {args.output}")


if __name__ == "__main__":
    main()
