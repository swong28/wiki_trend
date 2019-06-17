from preprocess import * 
# from neo4j_connector import * 

from py2neo import Node, Graph, Relationship
from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext

def processData():
    # Begin Spark Session
    spark = SparkSession.builder.appName("wiki-trend").getOrCreate()

    # Begin Spark Context
    sc = SparkContext.getOrCreate()

    sql_context = SQLContext(sc)

    # Pre-process Data
    # path2 = "./data/2016_shorted.tsv"
    path = "s3a://insight-wiki-clickstream/2016_04_en_clickstream.tsv"
    # path = "./data/2016_04_en_clickstream.tsv"
    raw = loadFiles(path, sc)
    wikiDF = cleanData(raw, spark)

    # Create Link Nodes
    sql_context.registerDataFrameAsTable(wikiDF, "wiki_clicks")

    # createLinkNodes(sql_context, sc)
    # temp = wikiDF.rdd.map(createRelationships)
    # print(wikiDF.show())
    
    wikiDF.rdd.map(createRelationships).collect()
    # for row in wikiDF.rdd.collect():
    #     createRelationships(row)
    
    # sc.parallelize(wikiDF.rdd.collect()).foreachPartition(createRelationships)

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

def createRelationships(row):
    gc = Graph('bolt://34.236.37.208:7687',
               password='wong1234')

    tx = gc.begin()
    # for row in rows:
    n1 = Node("Link", name=row['FROM'])
    n2 = Node("Link", name=row['TO'])
    rel = Relationship(n1, "SENT TO", n2)
    tx.merge(n1, "Link", "name")
    tx.merge(n2, "Link", "name")
    tx.merge(rel)
    tx.commit()

if __name__ == "__main__":
    processData()


