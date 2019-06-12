from pyspark.sql import SparkSession, SQLContext
from pyspark import SparkContext
from py2neo import Graph, Node, Relationship

def processData(sc, job_args=None):
    """
    Read data files from S3 bucket and write node entries to Neo4j
    """
    
    # Create a spark session for wiki-trend
    spark = SparkSession.builder.appName("wiki-trend").getOrCreate()

    # Create SQL context and read files from S3 bucket (locally for now)
    sql_context = SQLContext(sc)
    
    path = "./data/2016_04_en_clickstream.tsv"
    
    raw_file = spark.read.format("csv") \
        .option("header", "true") \
        .load(path)
    
    sql_context.registerDataFrameAsTable(raw_file, "Wiki_Clickstream")

def createSchema():
    """
    Create schema for neo4j database
    """

    ### To Be Continued ###


graph = Graph("bolt://localhost:7687",
    auth=("neo4j", "neo4j"))

if __name__ == "__main__":
    sc = SparkContext(appName='wiki-trend').getOrCreate()
    processData(sc)

