
# python sparksql_106_spark_localcluster.py \
#     --input_green=data/pq/green/2020/*/ \
#     --input_yellow=data/pq/yellow/2020/*/ \
#     --output=data/report-2020

### Using spark submit
# URL="spark://afro-de.europe-west1-b.c.afro-de-376122.internal:7077"

# spark-submit \
#     --master="${URL}" \
#     sparksql_106_spark_localcluster.py \
#         --input_green=data/pq/green/2021/*/ \
#         --input_yellow=data/pq/yellow/2021/*/ \
#         --output=data/report-2021

### Stopping master and workers
# ./sbin/stop-worker.sh
# # no org.apache.spark.deploy.worker.Worker to stop
# ./sbin/stop-master.sh
# # stopping org.apache.spark.deploy.master.Master

### arguments for gcp data cluster proc
```
--input_green=gs://afro-prefect-de/pq/green/2021/*/
--input_yellow=gs://afro-prefect-de/pq/yellow/2021/*/
--output=gs://afro-prefect-de/report-2021
```

### dataproc commands

```terminal
gcloud dataproc jobs submit pyspark \
    --cluster=afro-de-proc \
    --region=europe-west6 \
    gs://afro-prefect-de/code/sparksql_107_sparkg_cscluster.py \
    -- \
        --input_green=gs://afro-prefect-de//pq/green/2021/*/ \
        --input_yellow=gs://afro-prefect-de//pq/yellow/2021/*/ \
        --output=gs://afro-prefect-de//report-2021
```

### Spark and bigquery

dataproc-temp-europe-west6-535641511316-aqmcn5j8
spark.conf.set('temporaryGcsBucket', 'dataproc-temp-europe-west6-535641511316-aqmcn5j8')

```terminal
gcloud dataproc jobs submit pyspark \
    --cluster=afro-de-proc \
    --region=europe-west6 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://afro-prefect-de/code/sparksql_107_bigquery.py \
    -- \
        --input_green=gs://afro-prefect-de/pq/green/2020/*/ \
        --input_yellow=gs://afro-prefect-de/pq/yellow/2020/*/ \
        --output=spark.reports-2020



  - --output=spark.reports-2020
  jarFileUris:
  - gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar
  mainPythonFileUri: gs://afro-prefect-de/code/sparksql_107_bigquery.py
reference:
  jobId: 39c8b2fb0757426492d62170c66b2b68
  projectId: afro-de-376122
status:
  state: DONE
  stateStartTime: '2023-03-11T16:29:12.147713Z'
statusHistory:
- state: PENDING
  stateStartTime: '2023-03-11T16:28:13.429995Z'
- state: SETUP_DONE
  stateStartTime: '2023-03-11T16:28:13.494283Z'
- details: Agent reported job success
  state: RUNNING
  stateStartTime: '2023-03-11T16:28:13.901621Z'
yarnApplications:
- name: LocalSparkCluster_sparkSubmit
  progress: 1.0
  state: FINISHED
  trackingUrl: http://afro-de-proc-m:8088/proxy/application_1678536805502_0004/

  ```        