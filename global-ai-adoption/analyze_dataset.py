"""Reproduce the descriptive summaries used in the Tableau dashboards.

Python 3.9+; standard library only. Rates are already expressed on a 0-100 scale.
No causal effects or population-level market shares are estimated.
"""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean, median

ADOPTION = "AI Adoption Rate (%)"
REVENUE = "Revenue Increase Due to AI (%)"
JOB_LOSS = "Job Loss Due to AI (%)"
COLLABORATION = "Human-AI Collaboration Rate (%)"
MARKET = "Market Share of AI Companies (%)"
RATES = [ADOPTION, REVENUE, JOB_LOSS, COLLABORATION,
         "Consumer Trust in AI (%)", MARKET]


def grouped(rows, keys, metric=None, statistic="mean"):
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[key] for key in keys)].append(row)
    result = []
    for group, records in sorted(groups.items()):
        entry = dict(zip(keys, group))
        entry["n"] = len(records)
        if metric is not None:
            values = [float(record[metric]) for record in records]
            function = median if statistic == "median" else fmean
            entry[statistic] = round(function(values), 6)
        result.append(entry)
    return result


def analyze(path):
    raw = path.read_bytes()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        fields = reader.fieldnames
    required = {"Country", "Year", "Industry", "Regulation Status",
                "Top AI Tools Used", *RATES}
    if not fields or required.difference(fields):
        raise ValueError("Missing required fields: " + str(required.difference(fields or [])))
    if not rows:
        raise ValueError("The dataset is empty")
    missing = {field: sum(not row[field].strip() for row in rows) for field in fields}
    if any(missing.values()):
        raise ValueError("Resolve missing values before aggregation: " + str(missing))
    out_of_range = {field: sum(not 0 <= float(row[field]) <= 100 for row in rows)
                    for field in RATES}
    if any(out_of_range.values()):
        raise ValueError("Rate outside 0-100: " + str(out_of_range))
    counts = Counter(tuple(row[field] for field in fields) for row in rows)
    return {
        "source": "Atharva Soundankar, Impact of AI on Digital Media (2020-2025), Kaggle",
        "sha256": hashlib.sha256(raw).hexdigest(),
        "method": "Unweighted record means; annual job loss uses median; tool distributions use counts.",
        "limitations": "Sampling and observational provenance are undocumented. Results describe this sample only; no causal or population inference.",
        "quality": {
            "rows": len(rows), "fields": len(fields),
            "countries": len({row["Country"] for row in rows}),
            "industries": len({row["Industry"] for row in rows}),
            "years": sorted({row["Year"] for row in rows}),
            "missing_by_field": missing,
            "exact_duplicate_rows": sum(count - 1 for count in counts.values()),
            "out_of_range_rates": out_of_range,
        },
        "country_adoption": grouped(rows, ["Country"], ADOPTION),
        "country_regulation_adoption": grouped(rows, ["Country", "Regulation Status"], ADOPTION),
        "year_adoption": grouped(rows, ["Year"], ADOPTION),
        "year_revenue": grouped(rows, ["Year"], REVENUE),
        "year_job_loss": grouped(rows, ["Year"], JOB_LOSS, "median"),
        "industry_tool_counts": grouped(rows, ["Industry", "Top AI Tools Used"]),
        "year_industry_collaboration": grouped(rows, ["Year", "Industry"], COLLABORATION),
        "country_job_loss": grouped(rows, ["Country"], JOB_LOSS),
        "country_tool_recorded_market_metric": grouped(rows, ["Country", "Top AI Tools Used"], MARKET),
        "industry_revenue": grouped(rows, ["Industry"], REVENUE),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path,
                        default=Path(__file__).with_name("Global_AI_Content_Impact_Dataset.csv"))
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("analysis_summary.json"))
    args = parser.parse_args()
    result = analyze(args.csv)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Analyzed {result['quality']['rows']} rows; saved {args.output.name}")


if __name__ == "__main__":
    main()
