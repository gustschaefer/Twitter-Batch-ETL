from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *
import os
from config import temp_json_files, temp_parquet_files

sc = SparkSession.builder.appName("JsontoParquet").getOrCreate()

def json_to_parquet(temp_json_files=temp_json_files, temp_parquet_files=temp_parquet_files):

    for file in os.listdir(temp_json_files):
        if file.endswith(".json"):
            file_name = os.path.splitext(file)[0]
            path_json = os.path.join(temp_json_files, file)
            path_parquet = os.path.join(temp_parquet_files, file_name)
            df = sc.read.option("multiline","true").json(path_json)
            df.write.parquet(path_parquet)

	sc.stop()
