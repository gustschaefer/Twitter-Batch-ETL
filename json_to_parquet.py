from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *

sc = SparkSession.builder.appName("JsontoParquet").getOrCreate()

df = sc.read.option("multiline","true").json('test.json')
df.write.parquet('t.parquet')

sc.stop()
