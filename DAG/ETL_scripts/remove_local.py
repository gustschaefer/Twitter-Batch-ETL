import os
import shutil

def remove_local(temp_json_files, temp_parquet_files):
	paths = [temp_json_files, temp_parquet_files]
	for path in paths:
		if os.path.isdir(path):
			# remove pasta
			print("Antes: ", os.listdir(path))
			shutil.rmtree(path, ignore_errors=True)
			# refaz a pasta porem vazia
			os.makedirs(path)
			print("Agora: ", os.listdir(path))
			print(f"Arquivos de {path} foram removidos!")
		else:
			print(f"Não foi possível remover os arquivos, pois {path} nao é uma pasta...")
