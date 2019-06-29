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
        self.graph = Graph(os.environ.get('NEO4J_BOLT'),
                           password=os.environ.get('NEO4J_PASSWORD'))

if __name__ == '__main__':
    print(neo4jConnector().graph)