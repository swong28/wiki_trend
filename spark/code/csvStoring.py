from preprocessData import * 

from py2neo import Graph
from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext
import boto3
import time

def storeNeo4jFromS3(path):
    # Begin Spark Session
    spark = SparkSession.builder.appName("wiki-trend")\
            .config("spark.hadoop.fs.s3a.fast.upload","true")\
            .getOrCreate()

    # Begin Spark Context
    sc = SparkContext.getOrCreate()

    # Pre-process Data
    raw = loadFiles(path, sc)
    wikiDF = cleanData(raw, spark)

    # Export as CSV
    exportAsCSV(wikiDF)

    # s3 Bucket files to neo4j
    s3 = boto3.resource('s3')
    
    BUCKET_NAME = 'modified-clickstream-data'
    PREFIX = 'Output/p'
    my_bucket = s3.Bucket(BUCKET_NAME)

    for file in my_bucket.objects.all():
        if (file.key[:len(PREFIX)]==PREFIX):
            writeToDB(file.key)

def writeToDB(filename):
    gc = neo4jConnector().graph
    
    s3_link = "'https://modified-clickstream-data.s3.amazonaws.com/" \
        + filename + "'"
    gc.run("""
    USING PERIODIC COMMIT 
    LOAD CSV FROM """+s3_link+""" AS line
    MERGE (n1:Link {name: line[0]})
    MERGE (n2:Link {name: line[2]})
    CREATE (n1) -[r:SENT_TO {occurence: line[1]}]->(n2)
    """)

if __name__ == "__main__":
    start_time = time.time()
    path = "s3a://insight-wiki-clickstream/2016_04_en_clickstream.tsv"
    storeNeo4jFromS3(path)
    print("--- %s seconds Used ---" %(time.time()-start_time))
