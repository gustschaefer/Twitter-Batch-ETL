from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *
import os

sc = SparkSession.builder.appName("JsontoParquet").getOrCreate()

# paths
json_input_data_folder = "tweets-data/json"
parquet_output_data_folder = "tweets-data/parquet"

def json_to_parquet(json_input_data_folder, parquet_output_data_folder):

    for file in os.listdir(json_input_data_folder):
        if file.endswith(".json"):
            file_name = os.path.splitext(file)[0]
            path_json = os.path.join(json_input_data_folder, file)
            path_parquet = os.path.join(parquet_output_data_folder, file_name)
            df = sc.read.option("multiline","true").json(path_json)
            df.write.parquet(path_parquet)

json_to_parquet(json_input_data_folder, parquet_output_data_folder)
sc.stop()
