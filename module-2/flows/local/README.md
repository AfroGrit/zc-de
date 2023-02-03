### Running prefect locally

run pgadmin inside docker before data ingest script

```console
mkdir ny_taxi_data
docker run -d \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```