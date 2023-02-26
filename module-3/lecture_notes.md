# Data Warehouse and BigQuery

## BigQuery

BigQuery is a fully managed enterprise data warehouse that manage and analyze data with built-in features such as:

- M.L.
- Geospatial analysis
- B.I.
- Serverless data warehouse
- Software as well as infrastructure: **scalability** and **high-availability**
- Separate compute engine that analyzes data from storage
- On demand pricing: 1 TB of data processed is \$5
- Flat rate pricing:
  1. Based on number of pre requested slots
  2. 100 slots → \$2,000/month = 400 TB data processed on demand pricing.

### BigQuery commands

~~~~sql
-- Query public available table
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;

-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `taxi-rides-ny.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://nyc-tl-data/trip data/yellow_tripdata_2019-*.csv', 'gs://nyc-tl-data/trip data/yellow_tripdata_2020-*.csv']
);
~~~~

~~~~sql
-- Check yello trip data
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata limit 10;
~~~~

## BigQuery Partition

Segmentation of the database that improves query execution. BIgQuery partitions limit set at 4000.

- partitioned and non-partioned queries

~~~~sql
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_non_partitoned AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitoned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
~~~~

- size: partitioned and non-partioned DB

~~~~sql
-- Impact of partition
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_non_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
~~~~

- CRUD: partitioned DB

~~~~sql
-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `nytaxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitoned'
ORDER BY total_rows DESC;
~~~~

## BigQuery Clusterring

Clustered tables in BigQuery are tables that have a user-defined column sort order using clustered columns. Clustered tables can improve query performance and reduce query costs.

***A clustered column is a user-defined table property that sorts storage blocks based on the values in the clustered columns***


| **Clustering**                                                                        | **Partitoning**                       |
|---------------------------------------------------------------------------------------|---------------------------------------|
| Cost benefit unknown.                                                                 | Cost known upfront.                   |
| More granularity than partitioning allows.                             | Partition-level management.  |
| Queries use filters or aggregation on multiple columns. | Filter or aggregate on single column. |
| High cardinality in a column or group of columns    |                                       |

### Clustering over paritioning

Like clustering, partitioning uses user-defined partition columns to specify how data is partitioned and what data is stored in each partition. Unlike clustering, ***partitioning provides granular query cost estimates before you run a query.***

- Partitioning = small amount of data per partition ~> 1 GB).
- Partitioning = results in a large number of partitions beyond the limits on partitioned tables.
- Partitioning = results in your mutation operations modifying the majority of partitions in the table frequently (for example, every few minutes).
