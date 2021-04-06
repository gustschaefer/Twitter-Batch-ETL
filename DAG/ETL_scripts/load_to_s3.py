import os
import glob
from airflow.hooks.S3_hook import S3Hook
from config import bucket_name, temp_parquet_files

def local_to_s3(bucket_name=bucket_name, parquet_filepath=temp_parquet_files):
    s3 = S3Hook()

	for f in glob.glob(parquet_filepath):
		key = #TODO
		s3.load_file(filename=f, bucket_name=bucket_name, replace=True, key=key)

# Finalizar***