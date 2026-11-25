WITH ranked AS (
  SELECT athlete, edition, day, views,
    ROW_NUMBER() OVER (
      PARTITION BY athlete, edition ORDER BY views DESC, day
    ) AS position
  FROM daily
)
SELECT athlete, edition, day, views FROM ranked
WHERE position = 1 ORDER BY views DESC;

SELECT athlete, edition, event_day, ROUND(multiple, 1) AS lift
FROM daily WHERE event_day BETWEEN 0 AND 7
ORDER BY athlete, edition, event_day;

WITH ranked AS (
  SELECT article, views,
    ROW_NUMBER() OVER (PARTITION BY article ORDER BY views) AS rn
  FROM daily WHERE day BETWEEN '2024-07-01' AND '2024-07-07'
)
SELECT d.athlete, d.edition, ROUND(d.multiple, 1) AS lift14,
       ROUND(1.0 * d.views / r.views, 1) AS lift7
FROM daily d JOIN ranked r USING (article)
WHERE d.event_day = 3 AND r.rn = 4 ORDER BY d.athlete, d.edition;