
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
--input_green=gs://afro-prefect-de/pq/green/2021/*/
--input_yellow=gs://afro-prefect-de/pq/yellow/2021/*/
--output=gs://afro-prefect-de/report-2021

### dataproc commands
gcloud dataproc jobs submit pyspark \
    --cluster=afro-de-proc \
    --region=europe-west6 \
    gs://afro-prefect-de/code/sparksql_107_sparkg_cscluster.py \
    -- \
        --input_green=gs://afro-prefect-de//pq/green/2021/*/ \
        --input_yellow=gs://afro-prefect-de//pq/yellow/2021/*/ \
        --output=gs://afro-prefect-de//report-2021

