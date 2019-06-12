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

from pyspark import SparkContext
from pyspark.sql import SparkSession

# sc =SparkContext().getOrCreate()
path = "s3a://insight-wiki-clickstream/2016_04_en_clickstream.tsv"
path2 = "./data/2016_04_en_clickstream.tsv"
# raw = sc.textFile(path)
# print(raw.first())


def loadFiles(bucket_name):
    """
    Load files in a aws bucket with name, bucket_name.
    """
    return sc.textFile(bucket_name)

def cleanData(spark_file):
    """
    Clean Wikipedia Clickstream Data
    """

    # Skip the Header
    raw.first()

    # Seperate the values by tabs
    parts = raw.map(lambda x: x.split('\t'))
    
    # Define Schema
    

    # Add Structure Fields


if __name__ == '__main__':
    sc = SparkContext().getOrCreate()
    raw = loadFiles(path)

