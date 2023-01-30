### Q.1

```console
docker build --help
--iidfile string          Write the image ID to the file
```

### Q.2

```console
docker run -it --entrypoint=bash python:3.9
root@8edabe49d966:/# pip list
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
```

Run postgres

```console
mkdir hw_1_green_data

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="hw_1_green_ny_taxi" \
  -v $(pwd)/hw_1_green_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

pgcli -h localhost -p 5432 -u root -d hw_1_green_ny_taxi
```

NB - Roughly 3 minute to ingest the data into postgres

### Q.3

How many taxi trips were totally made on January 15?

```console
SELECT COUNT(*)
 FROM hw_1_green_tripdata_201901
 WHERE lpep_pickup_datetime::date='2019-01-15';

+-------+
| count |
|-------|
| 22453 |
+-------+
SELECT 1
Time: 0.165s
```

### Q.4

Which was the day with the largest trip distance Use the pick up time for your calculations.

```console
SELECT MAX(trip_distance), lpep_pickup_datetime::date
FROM hw_1_green_tripdata_201901
GROUP BY lpep_pickup_datetime::date
ORDER BY MAX(trip_distance) DESC
LIMIT 3;
+--------+----------------------+
| max    | lpep_pickup_datetime |
|--------+----------------------|
| 117.99 | 2019-01-15           |
| 80.96  | 2019-01-18           |
| 64.27  | 2019-01-28           |
+--------+----------------------+
SELECT 3
Time: 0.353s
hw_1_green_ny_taxi>
```

### Q.5

```console
HAVING passenger_count in (2, 3);
+-----------------+------------+
| passenger_count | trip_count |
|-----------------+------------|
| 2.0             | 1283       |
| 3.0             | 256        |
+-----------------+------------+
SELECT 2
Time: 0.283s
hw_1_green_ny_taxi>
```

### Q.6

```console
 LIMIT 1;
+-------------------------------+-------------+
| dropoff_zone                  | largest_tip |
|-------------------------------+-------------|
| Long Island City/Queens Plaza | 88.0        |
+-------------------------------+-------------+
SELECT 1
Time: 0.322s
hw_1_green_ny_taxi>

```
