import os
import shutil

def remove_local(temp_json_files, temp_parquet_files):
	json_parquet_paths = [temp_json_files, temp_parquet_files]
	for path in paths:
		if os.path.isdir(path):
			# remove pasta
			shutil.rmtree(path, ignore_errors=True)
			# refaz a pasta porem vazia
			os.makedirs(path)
		else:
			print(f"Não foi possível remover os arquivos, pois {path} nao é uma pasta...")
