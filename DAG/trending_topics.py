# Default
from datetime import datetime, timedelta
import os

# Airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

# Tasks
from ETL_scripts.load_to_s3 import local_json_to_s3, local_parquet_to_s3
from ETL_scripts.extract_tweets import extract_trending_tweets
from ETL_scripts.remove_local import remove_local
from ETL_scripts.json_to_parquet import json_to_parquet

# Config
from ETL_scripts.config import consumer_key, consumer_secret, access_token, access_token_secret
from ETL_scripts.config import bucket_name, temp_json_files, temp_parquet_files
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day - 1),
    "retries": 0,
}

with DAG(
	"Twitter_Batch_ETL", 
	schedule_interval=timedelta(minutes=1),
	catchup=False,
	default_args=default_args
) as dag:

	start = DummyOperator(task_id='start', dag=dag)

	extract_trending = PythonOperator(
		task_id='extract_trending',
		python_callable=extract_trending_tweets,
		op_kwargs={
		    'temp_json_files': temp_json_files,
		    'num_tweets': 10,
		    'CONSUMER_KEY': consumer_key, 
		    'CONSUMER_SECRET': consumer_secret, 
		    'ACCESS_TOKEN': access_token, 
		    'ACCESS_TOKEN_SECRET': access_token_secret
		},
	)

	spark_transform_json2parquet = PythonOperator(
		task_id='spark_transform_json2parquet',
		python_callable=json_to_parquet,
		op_kwargs={
			'temp_json_files': temp_json_files,
			'temp_parquet_files': temp_parquet_files
		},
		dag=dag
	)

	load_json_trending_to_s3 = PythonOperator(
		task_id='load_json_trending_format_to_s3',
		python_callable=local_json_to_s3,
		op_kwargs={
			'bucket_name': bucket_name,
			'j_filepath': temp_json_files
		},
	)

	load_parquet_trending_to_s3 = PythonOperator(
		task_id='load_parquet_trending_format_to_s3',
		python_callable=local_parquet_to_s3,
		op_kwargs={
			'bucket_name': bucket_name, 
			'p_filepath': temp_parquet_files
		},
	)
    
	remove_local_files = PythonOperator(
		task_id='remove_local_files',
		python_callable=remove_local,
		op_kwargs={
			'temp_json_files': temp_json_files,
			'temp_parquet_files': temp_parquet_files
		},
	)

	end = DummyOperator(task_id='end_of_data_pipeline', dag=dag)

# Airflow pipeline
start >> extract_trending >> spark_transform_json2parquet >> [load_json_trending_to_s3, load_parquet_trending_to_s3] >> remove_local_files >> end
