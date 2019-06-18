from py2neo import Graph

def pageRank(graph, wiki_page):
    tx = graph.begin()
    tx.run(
    """
    CALL algo.pageRank.stream(
        'MATCH (:Link {name:"Chicago"})-[*1..3]-(p:Link)
            RETURN DISTINCT id(p) AS id',
        'MATCH (p1:Link)-[r]->(p2:Link) 
            RETURN id(p1) AS source, id(p2) AS target, r.occurence AS weight',
        {
        graph: 'cypher', 
        iterations:20, 
        dampingFactor:0.85
        })

    YIELD nodeId, score
        
    RETURN algo.asNode(nodeId).name AS page,score
    ORDER BY score DESC
    """
    )
    tx.commit()
    return tx

def centrality(graph, wiki_page):
    return 

if __name__ == "__main__":
    gc = Graph('bolt://3.217.252.116',
               password='wong1234')
    temp = pageRank(gc, 'Barack_Obama')
    print(temp.run())
    # pageRank(gc, "Barack_Obama")
