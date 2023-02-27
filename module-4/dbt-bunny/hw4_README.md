# Homework 4: Analytics engineering

practicals ver 2

## q.1

```sql
SELECT COUNT(*) FROM `afro-de-376122.productions.fact_trips`;
-- 61619945
```

## q.2

89.9/10.1

## q.3

```sql
SELECT date_trunc(pickup_datetime, YEAR), count(*)
FROM `afro-de-376122.afrodbt.dbt-fhv` 
GROUP BY 1
ORDER BY 1 DESC;
1. 2020-01-01 00:00:00 UTC 14914817
2	2019-01-01 00:00:00 UTC 43244696
```

## q.4

```sql
SELECT date_trunc(pickup_datetime, YEAR), count(*)
FROM `afro-de-376122.afrodbtdataset.fact_fhv_trips`
GROUP BY 1
ORDER BY 1 DESC;
-- 
2020-01-01 00:00:00 UTC | 2645439
2019-01-01 00:00:00 UTC | 22998722
```

## q.5

January ~ from the dashboard
