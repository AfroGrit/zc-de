# Week 2 Homework

workflow orchestration and observation

Start Prefect Orion.

```console
prefect orion start
```

https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-01.csv.gz


prefect deployment build hw_2_param_flow.py:hw_2_etl_parent_flow -n "HW2 Param ETL"
prefect deployment apply hw_2_etl_parent_flow-deployment.yaml
prefect agent start -q 'default'

## q.1

```console
congestion_surcharge            float64
dtype: object
09:03:53.445 | INFO    | Task run 'clean-b9fd7e03-0' - rows: 447770
09:03:53.485 | INFO    | Task run 'clean-b9fd7e03-0' - Finished in state Completed()
09:03:53.530 | INFO    | Flow run 'quartz-nyala' - Created task run 
```
