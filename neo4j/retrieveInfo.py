from py2neo import Graph
from neo4j_connector import neo4jConnector

def pageRank(graph, wiki_page):
    """
    Run the build in pageRank algorithm from Neo4J server.
    """
    
    return graph.run(
    '''
    CALL algo.pageRank.stream(
        'MATCH (:Link {name:"'''+wiki_page+'''"})-[*1]-(p:Link)
            RETURN DISTINCT id(p) AS id',
        'MATCH (p1:Link)-[r]->(p2:Link) 
            RETURN id(p1) AS source, id(p2) AS target, r.OCCURENCE AS weight',
        {
        graph: 'cypher', 
        iterations:10, 
        dampingFactor:0.7
        })

    YIELD nodeId, score
        
    RETURN algo.asNode(nodeId).name AS page,score
    ORDER BY score DESC
    LIMIT 5
    '''
    )

if __name__ == "__main__":
    gc = neo4jConnector().graph
    print(gc)
    temp = pageRank(gc, 'Chicago')
    print(temp.to_data_frame())
    # pageRank(gc, "Barack_Obama")
