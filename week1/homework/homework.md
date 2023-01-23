### Short answers
1. `--iidfile string`
2. 3
3. 20530
4. 2019-01-15
5. 2: 1282 ; 3: 254
6. Long Island City/Queens Plaza



## Week 1 Homework

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file* 

- `--imageid string`
- `--iidfile string` 
- `--idimage string`
- `--idfile string`

## Answer 1 - `--iidfile string`
```docker build --help | grep "Write the image ID to the file```

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

- 1
- 6
- 3
- 7

## Answer 2.1 - 3
```docker run -it --entrypoint="bash" python:3.9```
```python -m pip list --format=freeze```
```python -m pip list --format=freeze | wc -l``` 
Итого 3 строки

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from January 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

## Answer 2.2
Ports 5432 and 8080 are forwarded already.
```mkdir ~/git/de-zoomcamp2023/week1/homework && cd homework```
```cp ../docker-compose.yaml .```
```docker network create external-network```
```code docker-compose.yaml```

append external network block and save:
```
networks: 
  default:  
    name: external-network
    external: true
```
```docker-compose up -d```
```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz```
```gzip -d green_tripdata_2019-01.csv.gz```
```less green_tripdata_2019-01.csv``` Ctrl+Z then
```cp ../upload-data.py .```
```code upload-data.py```

put on top basic extension handler
```
if '.gz' in url:
        os.system(f'wget {url} -O {csv_name_gz}')
        os.system(f'gzip -fd {csv_name_gz}')
    elif '.csv' in url:
        os.system(f'wget {url} -O {csv_name}')
    else:
        raise NameError('Something is wrong with file extension, it should be .csv or .csv.gz')
```

replaced .to_datatime blocks to less specific in terms of column names
```
for column in chunk:
            if 'date' in column or 'time' in column:
                chunk[[column]] = chunk[[column]].apply(pd.to_datetime, errors='coerce')
        chunk.to_sql(name=table_name, schema=schema_name, con=engine, if_exists='append')
```
```cp ../Dockerfile .```
```sudo docker build -t taxi_ingest:homework .``` reubilt docker container with updated python script
```sudo docker run -it \
  --network=external-network \
  taxi_ingest:homework \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --schema_name=public \
    --table_name=green_taxi_trips \
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
```
```sudo docker run -it \
  --network=external-network \
  taxi_ingest:homework \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --schema_name=public \
    --table_name=zones \
    --url="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
```
```pgcli -h localhost -p 5432 -U root -d ny_taxi```
```\dt```

## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 20689
- 20530
- 17630
- 21090

## Answer 3 - 20530
in pgcli:
```select count(1), cast(lpep_pickup_datetime as date) dt from public.green_taxi_trips where cast(lpep_dropoff_datetime as date) = '2019-01-15' and c
 ast(lpep_pickup_datetime as date) = '2019-01-15' group by cast(lpep_pickup_datetime as date);
```

## Question 4. Largest trip for each day - 2019-01-15

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-18
- 2019-01-28
- 2019-01-15
- 2019-01-10

```
select tr.trip_distance, cast(tr.lpep_pickup_datetime as date) dt  from public.green_taxi_trips tr order by tr.trip_distance desc limit 1;
```

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- 2: 1282 ; 3: 254
- 2: 1282 ; 3: 274

## Answer 5 - 2: 1282 ; 3: 254
```
select count(1), tr.passenger_count, cast(tr.lpep_pickup_datetime as date) dt  from public.green_taxi_trips tr where cast(tr.lpep_pickup_datetime 
 as date) = '2019-01-01' group by cast(tr.lpep_pickup_datetime as date), tr.passenger_count having tr.passenger_count in (2,3);
```

## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- South Ozone Park
- Long Island City/Queens Plaza

## Answer 6 - Long Island City/Queens Plaza
```
select do_zone."Zone" from public.green_taxi_trips tr left join public.zones pu_zone on tr."PULocationID" = pu_zone."LocationID" left join public.
 zones do_zone on tr."DOLocationID" = do_zone."LocationID" where pu_zone."Zone" = 'Astoria' order by tr.tip_amount desc limit 1;
```

## Submitting the solutions

* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 26 January (Thursday), 22:00 CET


## Answer part B - terraform
```terraform init```
```(base) AlexRaz@de-zoomcamp23:~/git/de-zoomcamp2023/week1/homework/terraform$ terraform apply```

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "ME-WEST1"
      + project                    = "de-zoomcamp-2023-375411"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + dataset {
              + target_types = (known after apply)

              + dataset {
                  + dataset_id = (known after apply)
                  + project_id = (known after apply)
                }
            }

          + routine {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + routine_id = (known after apply)
            }

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "ME-WEST1"
      + name                        = "dtc_data_lake_de-zoomcamp-2023-375411"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }

      + website {
          + main_page_suffix = (known after apply)
          + not_found_page   = (known after apply)
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.