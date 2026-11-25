# Global AI Adoption in Digital Media

Two Tableau dashboards explore 200 sample records across 10 countries, 10 industries and 2020-2025.

- [Open dashboard 1](https://public.tableau.com/views/GlobalAIAdoption_v2024_2_17955362613900/Dashboard?:showVizHome=no&:embed=true&:language=en-US): country adoption, country-by-regulation comparisons, yearly summaries and industry tool counts.
- [Open dashboard 2](https://public.tableau.com/views/GlobalAIAdoption_v2024_2_17955362613900/Dashboard2?:showVizHome=no&:embed=true&:language=en-US): collaboration, country-level adoption and job-loss means, recorded market-share metrics and industry revenue summaries.
- [Download the packaged workbook](Global%20AI%20Adoption_v2024.2.twbx).

## Question and method

How do recorded AI adoption rates and regulation labels differ across countries? Can the regulation labels be interpreted as exclusive country categories?

The workbook embeds the source extract. Rate charts use **unweighted arithmetic means of records**, with a **median** for the yearly job-loss summary. Tool distributions count records. The scatterplot uses one mark per country, showing mean adoption against mean reported job loss. Percentages stored on a 0-100 scale are displayed without multiplying by 100 again.

For example, the UK has records under all three regulation labels: mean adoption is 76.12% for Moderate (7 records), 59.32% for Strict (6), and 57.88% for Lenient (7). These labels vary within a country and should not be read as mutually exclusive national policies.

## Reproduce the summaries

Python 3.9+ is sufficient; no third-party packages are needed.

```sh
python analyze_dataset.py
```

This checks missing values, exact duplicates and percentage ranges, then writes `analysis_summary.json`. Every group includes its record count. The checked-in JSON was generated from the included CSV. The two dashboards and the downloadable workbook use the same data and aggregation rules.

## Data source and limits

Dataset: **Atharva Soundankar, Impact of AI on Digital Media (2020-2025)**, [Kaggle](https://www.kaggle.com/datasets/atharvasoundankar/impact-of-ai-on-digital-media-2020-2025), Apache License 2.0. The source CSV is redistributed unchanged; see [DATA_LICENSE.txt](DATA_LICENSE.txt).

The publisher does not document a sampling frame or observational provenance. These figures describe the provided sample, not national adoption estimates or measured global tool market shares. The column called "Market Share of AI Companies (%)" is shown as a recorded dataset metric only. Group sizes differ; yearly changes do not establish a real-world turning point. No causal effects are inferred.

Data preparation, validation code and workbook revisions were completed by Junyan Deng with OpenAI Codex assistance.
