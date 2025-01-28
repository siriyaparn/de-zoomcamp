#!/usr/bin/env python
# coding: utf-8

# Import module
import os
import pandas as pd
import psycopg2
import argparse
from time import time
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    table_name2 = params.table_name2
    url = params.url
    url2 = params.url2
    
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
        
    if url2.endswith('.csv.gz'):
        csv_name2 = 'output2.csv.gz'
    else:
        csv_name2 = 'output2.csv'

    os.system(f"wget {url} -O {csv_name}")
    os.system(f"wget {url2} -O {csv_name2}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Import data to DB
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df_look = pd.read_csv(csv_name2)
    df_look.rename(columns={'LocationID': 'locationid'}, inplace=True)
    df_look.rename(columns={'Borough': 'borough'}, inplace=True)
    df_look.rename(columns={'Zone': 'zone'}, inplace=True)
    
    df = next(df_iter)

    # Clean data from text to datetime
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.rename(columns={'RatecodeID': 'ratecodeid'}, inplace=True)
    df.rename(columns={'PULocationID': 'pulocationid'}, inplace=True)
    df.rename(columns={'DOLocationID': 'dolocationid'}, inplace=True)

    # First table
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # Second table
    df_look.head(n=0).to_sql(name=table_name2, con=engine, if_exists='replace')
    df_look.to_sql(name=table_name2, con=engine, if_exists='append')

    # Create loop to import data of each chunk to DB 
    while True: 

        try:
            t_start = time()
            
            df = next(df_iter)

            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df.rename(columns={'RatecodeID': 'ratecodeid'}, inplace=True)
            df.rename(columns={'PULocationID': 'pulocationid'}, inplace=True)
            df.rename(columns={'DOLocationID': 'dolocationid'}, inplace=True)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--table_name2', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')
    parser.add_argument('--url2', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)