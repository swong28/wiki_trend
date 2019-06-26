var viz;
function draw(wikipedia_page) {
    var config = {
        container_id: "viz",
        server_url: "bolt://3.220.71.43:7687",
        server_user: "neo4j",
        server_password: "wong1234",
        labels: {
            "Link": {
                "caption": "name",
                "size": "pagerank"
            }
        },
        relationships: {
            "SENT_TO": {
                "thickness": "OCCURENCE",
                "caption": false
            }
        },
        initial_cypher: 'MATCH (n {name:"'+wikipedia_page+'"})-[r:SENT_TO]->(m) RETURN * ORDER BY r.OCCURENCE DESC LIMIT 50'
    };
    config.labels["name"] = {
        "caption": "name",
        "size": "pagerank",
        "community": "community",
    };
    config.relationships["SENT_TO"] = {
        "thickness": "OCCURENCE",
        "caption": false,
    }
    viz = new NeoVis.default(config);
    viz.render();
    console.log(viz);
}

function stabilize() {
    viz.stabilize();
}