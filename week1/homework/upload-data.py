#!/usr/bin/env python
# coding: utf-8

import os
import argparse

import pandas as pd
from time import time
from sqlalchemy import create_engine
import psycopg2

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    schema_name = params.schema_name
    table_name = params.table_name
    url = params.url
    csv_name_gz = 'data.csv.gz'
    csv_name = 'data.csv'

    if '.gz' in url:
        os.system(f'wget {url} -O {csv_name_gz}')
        os.system(f'gzip -fd {csv_name_gz}')
    elif '.csv' in url:
        os.system(f'wget {url} -O {csv_name}')
    else:
        raise NameError('Something is wrong with file extension, it should be .csv or .csv.gz')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # (re)creating table
    chunk = next(df_iter)
    for column in chunk:
        if 'date' in column or 'time' in column:
            chunk[[column]] = chunk[[column]].apply(pd.to_datetime, errors='coerce')
    chunk.to_sql(name=table_name, schema=schema_name, con=engine, if_exists='replace')

    print('Everything is ready for ingestion')

    # loop will start from the begining of dataset
    for chunk in df_iter:
        st_time = time()
        
        for column in chunk:
            if 'date' in column or 'time' in column:
                chunk[[column]] = chunk[[column]].apply(pd.to_datetime, errors='coerce')
        chunk.to_sql(name=table_name, schema=schema_name, con=engine, if_exists='append')
        
        end_time = time()
        
        print('successfully ingested another %.0f rows of data for %.3f seconds' % (len(chunk), end_time-st_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
        
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='table name for postgres')
    parser.add_argument('--schema_name', help='schema name for postgres')
    parser.add_argument('--url', help='url for the csv.gz')

    args = parser.parse_args()

    main(args)


# python upload-data.py \
#   --user=root \
#   --password=root \
#   --host=localhost \
#   --port=5432 \
#   --db=ny_taxi \
#   --schema_name=public \
#   --table_name=yellow_taxi_trips \
#   --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
