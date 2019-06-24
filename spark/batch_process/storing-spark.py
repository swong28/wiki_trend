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
    # path = "s3a://insight-wiki-clickstream/2016_04_en_clickstream.tsv"
    path = "./data/shortened.tsv"

    raw = loadFiles(path, sc)
    wikiDF = cleanData(raw, spark)

    # Create Link Nodes
    sql_context.registerDataFrameAsTable(wikiDF, "wiki_clicks")

    # createLinkNodes(sql_context, sc)
    # temp = wikiDF.rdd.map(createRelationships)
    # print(wikiDF.show())
    
    createLinkNodes(sql_context, sc)
    wikiDF.rdd.foreachPartition(createRelationships)

def createLinkNodes(sql_context, sc):
    distinct_links = sql_context.sql("""
        SELECT DISTINCT(derivedtable.NewColumn)
        FROM
        ( 
            SELECT FROM as NewColumn FROM wiki_clicks 
            UNION
            SELECT TO as NewColumn FROM wiki_clicks 
        ) derivedtable
        WHERE derivedtable.NewColumn IS NOT NULL
    """)
    link_nodes = distinct_links.rdd.map(
        lambda x: (Node("Link", name=x['NewColumn'])))
    
    link_nodes.foreachPartition(createNodes)

def createNodes(partition):
    gc = Graph('bolt://localhost:7687',
                password='wong1234')

    
    for node in partition:
        tx = gc.begin()
        try:
            tx.create(node)
        except:
            # It means the node is already created in the database before
            continue
        tx.commit()
    

def createRelationships(rows):
    gc = Graph('bolt://localhost:7687',
               #'bolt://3.218.43.43:7687',
               password='wong1234')

    if (rows == None):
        return 
        
    tx = gc.begin()
    for row in rows:
        
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

        rel = Relationship(n1, "SENT_TO", n2, 
                        timestamp=timestamp, 
                        occurence=row['OCCURENCE'])
        tx.create(rel)
    tx.commit()

if __name__ == "__main__":
    start_time = time.time()
    processData()
    print("--- %s seconds Used ---" %(time.time()-start_time))
