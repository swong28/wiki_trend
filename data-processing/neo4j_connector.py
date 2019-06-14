"""
Jason Wong
6/12/2019
Wiki Trend

Create a connector that can process Spark data to Neo4j database
"""

from py2neo import Graph
import os 

class neo4jConnector():
    """
    Connector for neo4j database from Spark
    """

    def __init__(self):
        """
        Initialize neo4j connector with my neo4j username and password.
        """
        self.graph = Graph(password='wong1234')

    def close(self):
        """
        Close the neo4j database
        """
        self._diver.close()
    
    @classmethod
    def createNode(cls, tx, link):
        """
        Create nodes on the neo4j for each line in partition.
        """
        tx.run("MERGE (a:Link {name: $link})", link=link)

    @classmethod
    def defineRelationship(cls, tx, link_a, link_b, occurence):
        """
        Define Relationship beteen links
        """
        tx.run("MATCH (a:Link {name: $link_a}"
               "MATCH (b:Link {name: $link_b}"
               "MERGE (a)-[:OCCURRED]->(b)",
                link_a=link_a, link_b=link_b)