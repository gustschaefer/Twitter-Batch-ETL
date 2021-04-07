import os
import shutil
from config import temp_json_files, temp_parquet_files

json_parquet_paths = [temp_json_files, temp_parquet_files]

def remove_local(paths=json_parquet_paths):
	for path in paths:
		# remove pasta
		shutil.rmtree(path, ignore_errors=True)
		# refaz a pasta porem vazia
		os.mkdir(path)
