"""
Jason Wong
6/12/2019
Wiki Trend

Create a connector that can process Spark data to Neo4j database
"""

from neo4j import GraphDatabase
# from py2neo.database import Schema
import os 

class neo4jConnector():
    """
    Connector for neo4j database from Spark
    """

    def __init__(self):
        """
        Initialize neo4j connector with my neo4j username and password.
        """
        self._driver = GraphDatabase.driver(
            os.environ['NEO4J_URI'],
            auth=(os.environ['NEO4J_USER'], 
                password=os.environ['NEO4J_PASSWORD'])
        )

    def close(self):
        """
        Close the neo4j database
        """
        self._diver.close()
    
    def createNode(self, partition):
        """
        Create nodes on the neo4j for each line in partition.
        """
        for node in partition:
            tx = self.connector.begin()
            tx.merge(node)
            tx.commit()

    def defineIndices(self):
        """
        define and create indices for nodes in neo4j database
        """
        db_schema = Schema(self.connector)

        # To Be Continued
