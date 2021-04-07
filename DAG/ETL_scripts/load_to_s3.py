import os
import glob
from airflow.hooks.S3_hook import S3Hook
#from config import bucket_name, temp_parquet_files

def local_to_s3(bucket_name, parquet_filepath):
	s3 = S3Hook()

	for f in os.walk(parquet_filepath):
		# Obtem o path que sera salvo no S3 -> ex.: trending_tweets/TweetsData-Brazil-2021-04-01/file.parquet
		key = 'trending_tweets/'+f[0].split('/')[-1]
		print(key)
		# Obtem -> ex.: temp/parquet/TweetsData-Brazil-2021-04-01
		parquet_dir = f[0] 
		# obtem apenas arquivos (nome) .parquet. Necessario pois o diretorio tambem salva _SUCCESS
		is_parquet = [p for p in f[2] if p.endswith(".parquet") or p.endswith(".parquet.crc")]

		for parquet_file in is_parquet:
			local_file_path = os.path.join(f[0], parquet_file)
			s3_file_path = os.path.join(key, parquet_file)

			# Carrega para o S3
			s3.load_file(filename=local_file_path, 
						 bucket_name=bucket_name, 
						 key=s3_file_path)
# Exemplos:
# local_file_path = temp/parquet/TweetsData-Brazil-2021-04-01/file.parquet
# s3_file_path = trending_tweets/TweetsData-Brazil-2021-04-01/file.parquet
