from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *

sc = SparkSession.builder.appName("JsontoParquet").getOrCreate()

df = sc.read.json('tweet-data/json/TweetsData-Brazil-2021-03-29.json')
#df.write.parquet('tweet-data/parquet/t.parquet')

context.stop()