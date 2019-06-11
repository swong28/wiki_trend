"""
Jason Wong
June 10, 2019
Wiki Trend

This script reads all of the tsv files in an Aamzon S3 Bucket.

The main function

Args:
    item1
    item2

Returns:
    Description of the return

"""

# from pyspark import SparkContext, SparkConf
# from pyspark.sql import SparkSession

# import sys 

# path = "s3://insight-wiki-clickstream/2016_04_en_clickstream.tsv"

# sc = SparkContext.getOrCreate()
# spark = SparkSession(sc)

# df = spark.read.load(path)

# print(df)

from pyspark import SparkContext

# from pyspark.sql import HiveContext, SQLContext, Row
# from pyspark.sql.types import *
# from datetime import datetime
# from pyspark.sql.functions import col, date_sub, log, mean, to_date, udf, unix_timestamp
# from pyspark.sql.window import Window
# from pyspark.sql import DataFrame

sc =SparkContext().getOrCreate()
# sc.setLogLevel("DEBUG")
# sqlContext = SQLContext(sc)
path = "s3a://insight-wiki-clickstream/2016_04_en_clickstream.tsv"
raw = sc.textFile(path)
print(raw.first())