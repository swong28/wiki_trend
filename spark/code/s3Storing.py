from preprocessData import * 

from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext

import boto3
import time

def processData(path, processNode=False):
    # Begin Spark Session
    spark = SparkSession.builder.appName("wiki-trend")\
            .config("spark.hadoop.fs.s3a.fast.upload","true")\
            .getOrCreate()

    # Begin Spark Context
    sc = SparkContext.getOrCreate()

    sql_context = SQLContext(sc)

    # Pre-process Data

    raw = loadFiles(path, sc)
    wikiDF = cleanData(raw, spark)

    sql_context.registerDataFrameAsTable(wikiDF, "wiki_clicks")

    if (processNode):
        # Export Nodes CSV
        link_nodes = createLinkNodes(sql_context, sc)
        link_nodes = link_nodes.withColumnRenamed("NAME", ":ID(Link)")\
            .withColumnRenamed("PROPERTY_NAME", "name")

        link_nodes.repartition(1)\
            .write.format("com.databricks.spark.csv")\
            .mode("Append")\
            .option("header", "true")\
            .save("s3a://modified-clickstream-data/output/nodes/")
    
    # Export Relationship CSV
    nodes_relationship = createRelationship(sql_context, sc, path)
    nodes_relationship = nodes_relationship.withColumnRenamed("FROM", ":START_ID(Link)")\
        .withColumnRenamed("TO", ":END_ID(Link)")\
        .withColumnRenamed("OCCURENCE", "OCCURENCE:INT")

    nodes_relationship\
        .write.format("com.databricks.spark.csv")\
        .mode("Append")\
        .option("header", "false")\
        .save("s3a://modified-clickstream-data/output/relationships/")

def processFiles(folderPath, nodePath, fileType):
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(folderPath)

    for file in my_bucket.objects.all():
        if (file[-4:] != fileType):
            continue
        
        print("BEGIN PROCESSING FILE: ", file)
        if (nodePath == file):
            processData(folderPath+file, True)
        else:
            try:
                processData(folderPath+file)
            except:
                continue
        print("FINISHED PROCESSING FILE: ", file)
        

def createLinkNodes(sql_context, sc):
    distinct_links = sql_context.sql("""
        SELECT DISTINCT(derivedtable.NAME), derivedtable.NAME AS PROPERTY_NAME
        FROM
        ( 
            SELECT FROM as NAME FROM wiki_clicks 
            UNION
            SELECT TO as NAME FROM wiki_clicks 
        ) derivedtable
        WHERE derivedtable.NAME IS NOT NULL
    """)
    
    return distinct_links

def createRelationship(sql_context, sc, filename):
    timestamp = filename[-11:-4] + '-01'
    relationships = sql_context.sql("""
        SELECT *, '"""+timestamp+"""' AS TIME
        FROM wiki_clicks
        """)
    
    return relationships

if __name__ == "__main__":
    start_time = time.time()
    FOLDER_PATH = "s3a://insight-wiki-clickstream"
    FILE = "clickstream-enwiki-2019-05.tsv"
    PREFIX = ".tsv"
    processFiles(FOLDER_PATH, FILE, PREFIX)
    print("--- %s seconds Used ---" %(time.time()-start_time))
