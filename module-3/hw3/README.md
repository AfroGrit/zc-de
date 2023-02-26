# Homework: Data Warehouse and BigQuery

<b><u>Important Note:</b></u> <p>You can load the data however you would like, but keep the files in .GZ Format. 
If you are using orchestration such as Airflow or Prefect do not load the data into Big Query using the orchestrator.</br> 
Stop with loading the files into a bucket. </br></br>
<u>NOTE:</u> You can use the CSV option for the GZ files when creating an External Table</br>

<b>SETUP:</b></br>
Create an external table using the fhv 2019 data. </br>
Create a table in BQ using the fhv 2019 data (do not partition or cluster this table). </br>
Data can be found here: https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv </p>


## Setup

~~~~sql
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE afrobq.fhv_ext
OPTIONS (
  format = 'parquet',
  uris = ['gs://afro-prefect-de/data/fhv/fhv_tripdata_2019-*.parquet']
);

-- -- Check fhv external data
SELECT * FROM afrobq.fhv_ext limit 10;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE afrobq.fhv_non_partitoned AS
SELECT * FROM afrobq.fhv_ext;

-- -- Check fhv non partitioned data
SELECT * FROM afrobq.fhv_non_partitoned limit 10;
~~~~

## q.1

What is the count for fhv vehicle records for year 2019?

43244696

~~~~sql
SELECT
  COUNT(*) AS totalvehicle,
FROM
  afrobq.fhv_non_partitoned AS x
~~~~

## q.2

1. Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.

~~~~sql
SELECT
 COUNT(DISTINCT affiliated_base_number) AS count_distinct_ABN_ext
FROM afrobq.fhv_ext AS x;
-- 3164

SELECT
 COUNT(DISTINCT affiliated_base_number) AS count_distinct_ABN_non_partitoned
FROM afrobq.fhv_non_partitoned AS x;
-- 3164
~~~~

2. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

## q.3

~~~~sql
-- -- q.3
SELECT COUNT(*) from afrobq.fhv_non_partitoned
WHERE PUlocationID IS NULL AND DOlocationID IS NULL;
~~~~

## q.4

## q.5

~~~~sql
-- Create a partitioned table from external table
CREATE OR REPLACE TABLE afrobq.fhv_partitoned
PARTITION BY
  DATE(pickup_datetime) AS
SELECT * FROM afrobq.fhv_ext;

-- Impact of partition
-- Scanning 659.68 MB of data
SELECT DISTINCT(affiliated_base_number)
FROM afrobq.fhv_non_partitoned
WHERE DATE(pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~31.25 MB of DATA
SELECT DISTINCT(affiliated_base_number)
FROM afrobq.fhv_partitoned
WHERE DATE(pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';


-- Creating a partition and cluster table
CREATE OR REPLACE TABLE afrobq.fhv_partitoned_clustered
PARTITION BY DATE(pickup_datetime)
CLUSTER BY pickup_datetime AS
SELECT * FROM afrobq.fhv_ext;

-- Query scans 329.93 MB
SELECT count(*) as trips
FROM afrobq.fhv_partitoned
WHERE DATE(pickup_datetime) BETWEEN '2019-01-01' AND '2020-12-31';

-- Query scans 329.93 MB
SELECT count(*) as trips
FROM afrobq.fhv_partitoned_clustered
WHERE DATE(pickup_datetime) BETWEEN '2019-01-01' AND '2020-12-31';
~~~~

## q.6

querying data stored outside of BigQuery.

1. Cloud Bigtable
2. Cloud Storage
3. Google Drive

## q.7 

It is best practice in Big Query to always cluster your data.

```False```
