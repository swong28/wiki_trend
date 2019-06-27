from pyspark import SparkContext
from pyspark.sql import SparkSession, Row, SQLContext
import os 

from py2neo import Graph 

def loadFiles(bucket_name, sc):
    """
    Load files in a aws bucket with name, bucket_name.
    """
    return sc.textFile(bucket_name)

def cleanData(raw, spark):
    """
    Clean Wikipedia Clickstream Data
    """

    # Skip the Header
    header = raw.first()
    raw = raw.filter(lambda x: x != header)
    
    # Seperate the values by tabs
    #neo4j-admin doesn't support: quotes next to each other and escape quotes with '\""'
    parts = raw.map(lambda x: x.replace("\r","").replace("\"", "").replace("\\", "").replace('"','').replace(',',''))
    parts = parts.map(lambda x: x.split('\t'))
        
    # filter empty rows
    parts = parts.filter(lambda x: len(x) == 4)
    parts = parts.filter(lambda x: (x[0]!='' and x[1]!='' 
                                    and x[2]!='' and x[3]!=''))
    parts = parts.filter(lambda x: (x[0] not in ['other-search', 'other-internal', 'other-empty', 'other-external']) and
                                   (x[2] not in ['external']) and 
                                    (int(x[3]) > 0))
    
    # Define Schema
    links = parts.map(lambda p: Row(FROM=p[0],
                                    TO=p[1],
                                    TYPE=p[2],
                                    OCCURENCE=int(p[3]))) 

    # Convert to dataframe
    wikiDF = spark.createDataFrame(links)
    return wikiDF

def exportAsCSV(data_frame, path_name):
    """
    Export from Spark to CSV files and save to s3.
    """

    data_frame.write.format("csv").save(path_name)
    print('SUCCESS')
    return 

class neo4jConnector():
    """
    Connector for neo4j database from Spark
    """

    def __init__(self):
        """
        Initialize neo4j connector with my neo4j username and password.
        """
        self.graph = Graph(os.environ.get('NEO4J_BOLT'),
                           password=os.environ.get('NEO4J_PASSWORD'))

if __name__ == '__main__':
    path = "s3a://insight-wiki-clickstream/2016_04_en_clickstream.tsv"

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

    print(wikiDF.head(5))
    # exportAsCSV(wikiDF)
