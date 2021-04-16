from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import os

def json_to_parquet(temp_json_files, temp_parquet_files):
        
    print('Criando SparkSession...')
    sc = SparkSession.builder.appName("SparkJson2Parquet").getOrCreate()
    print('SparkSession...OK!')
	
    # Garante que a pasta destinada aos arquivos .parquet existe
    if not os.path.isdir(temp_parquet_files):
        os.makedirs(temp_parquet_files)
        print(f"New {temp_parquet_files} folder created!")

    for file in os.listdir(temp_json_files):
        if file.endswith(".json"):
            file_name = os.path.splitext(file)[0]
            path_json = os.path.join(temp_json_files, file)
            path_parquet = os.path.join(temp_parquet_files, file_name)
            df = sc.read.option("multiline","true").json(path_json)
            df.write.mode("overwrite").parquet(path_parquet)
            print(f"{path_json} convertido para parquet!")
			
    sc.stop()
    