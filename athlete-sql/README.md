# After the Medal: SQL analysis

This case explores daily Wikipedia readership for three Hong Kong medal winners at Paris 2024: Vivian Kong, Cheung Ka Long and Siobhan Haughey.

## Files

- `Olympics.sqlite`: SQLite database with 306 records, six articles and 51 dates, covering 1 July to 20 August 2024.
- `analysis.sql`: three read-only analytical queries using CTEs, window functions, filtering and a JOIN.

## Data structure

The `daily` table has the columns `athlete`, `edition`, `article`, `day`, `views`, `baseline`, `multiple`, and `event_day`. Its primary key is `(article, day)`.

`baseline` is the precomputed median daily views for 1-14 July. `multiple` is the day's views divided by that baseline. `event_day` aligns observations to the athlete's final medal date; Haughey's anchor is 31 July, following her second medal.

## Run the queries

Open the database with SQLite and execute `analysis.sql`. With the SQLite command-line client:

```sh
sqlite3 -header -column Olympics.sqlite < analysis.sql
```

The three queries return:

1. Six peak records, using `ROW_NUMBER()` to retain each article's peak date. Ties are resolved by the earlier date.
2. Forty-eight records for event days 0-7 across all six articles.
3. Six comparisons of day +3 multiples under the stored 14-day baseline and a seven-day baseline. For seven daily observations, the fourth value in ascending order is the median; this subset has seven observations per article.

The two highest peaks are Vivian Kong / ZH, 274,753 views on 28 July 2024, and Cheung Ka Long / ZH, 119,710 on 29 July 2024.

## Source and limits

Source: Wikimedia Pageviews API, `all-access`, `user`, daily granularity. [Example source response for Vivian Kong's English article](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Vivian_Kong/daily/20240701/20240820).

Pageviews can include repeat visits and do not measure unique readers. Language edition does not identify reader location. Low baseline traffic can generate large multiples, so absolute counts should be read alongside ratios. This is a descriptive case study of selected articles, with no causal claims.
