from py2neo import Graph

def pageRank(graph, wiki_page):
    return graph.run(
    '''
    CALL algo.pageRank.stream(
        'MATCH (:Link {name:"'''+wiki_page+'''"})-[*1..2]-(p:Link)
            RETURN DISTINCT id(p) AS id',
        'MATCH (p1:Link)-[r]->(p2:Link) 
            RETURN id(p1) AS source, id(p2) AS target, r.occurence AS weight',
        {
        graph: 'cypher', 
        iterations:30, 
        dampingFactor:0.7
        })

    YIELD nodeId, score
        
    RETURN algo.asNode(nodeId).name AS page,score
    ORDER BY score DESC
    LIMIT 5git
    '''
    )

def articleRank(graph, wiki_page):
    return graph.run(
    '''
    CALL algo.articleRank.stream(
        'MATCH (:Link {name:"'''+wiki_page+'''"})-[*1..2]-(p:Link)
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
    LIMIT 5
    '''
    )

if __name__ == "__main__":
    gc = Graph('bolt://3.217.252.116',
               password='wong1234')
    temp = articleRank(gc, 'Barack_Obama')
    print(temp.to_data_frame())
    # pageRank(gc, "Barack_Obama")
