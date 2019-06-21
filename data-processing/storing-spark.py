from preprocess import * 
# from neo4j_connector import * 

from py2neo import Node, Graph, Relationship
from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext

from datetime import date, datetime
import time

def processData():
    # Begin Spark Session
    spark = SparkSession.builder.appName("wiki-trend")\
            .config("spark.hadoop.fs.s3a.fast.upload","true")\
            .getOrCreate()

    # Begin Spark Context
    sc = SparkContext.getOrCreate()

    sql_context = SQLContext(sc)

    # Pre-process Data
    path = "s3a://insight-wiki-clickstream/2016_04_en_clickstream.tsv"
    # path = "./data/2016_04_en_clickstream.tsv"
    # path = "s3a://insight-wiki-clickstream/shortened.tsv"

    raw = loadFiles(path, sc)
    wikiDF = cleanData(raw, spark)

    # Create Link Nodes
    sql_context.registerDataFrameAsTable(wikiDF, "wiki_clicks")

    # createLinkNodes(sql_context, sc)
    # temp = wikiDF.rdd.map(createRelationships)
    # print(wikiDF.show())
    
    wikiDF.rdd.foreachPartition(createRelationships)

def createLinkNodes(sql_context, sc):
    distinct_links = sql_context.sql("""
        SELECT derivedtable.NewColumn 
        FROM
        ( 
            SELECT from as NewColumn FROM wiki_clicks 
            UNION
            SELECT to as NewColumn FROM wiki_clicks 
        ) derivedtable
        WHERE derivedtable.NewColumn IS NOT NULL
    """)
    link_nodes = distinct_links.rdd.map(
        lambda x: (Node("Link", name=x['NewColumn'])))
    
    sc.parallelize(link_nodes.collect()).foreachPartition(createRelationships)

def createNodes(partition):
    gc = Graph(password='wong1234')

    for node in partition:
        tx = gc.begin()
        tx.merge(node, "Link", "name")
    
    tx.commit()

def createRelationships(rows):
    gc = Graph(#'bolt://localhost:7687',
               'bolt://3.218.43.43:7687',
               password='wong1234')

    if (rows == None):
        return 
    
    for row in rows:
        tx = gc.begin()
        n1 = Node("Link", name=row['FROM'])
        n2 = Node("Link", name=row['TO'])

        try:
            tx.merge(n1, "Link", "name")
        except IndexError:
            print("This row's n1 contains error: ", row)
            continue
        
        try:
            tx.merge(n2, "Link", "name")
        except IndexError:
            print("This row's n2 contains error: ", row)
            continue 
        
        timestamp = '2016-04-01'
        #timestamp = date(*map(int, timestamp.split("-")))

        rel = Relationship(n1, "SENT_TO", n2, 
                        timestamp=timestamp, 
                        occurence=row['OCCURENCE'])
        tx.merge(rel)
        tx.commit()

if __name__ == "__main__":
    start_time = time.time()
    processData()
    print("--- %s seconds Used ---" %(time.time()-start_time))
