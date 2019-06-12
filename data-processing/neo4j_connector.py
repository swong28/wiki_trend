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
        self.connector = Graph(
            os.environ['NEO4J_DB'],
            secure=True,
            user=os.environ['NEO4J_USER'],
            password=os.environ['NEO4J_PASSWORD']
        )

    def createNode(self, partition):
        """
        Create nodes on the neo4j for each line in partition.
        """
        for node in partition:
            tx = self.connector.begin()
            tx.merge(node)
            tx.commit()