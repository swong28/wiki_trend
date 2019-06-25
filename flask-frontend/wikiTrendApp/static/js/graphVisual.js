var viz;
function draw(wikipedia_page) {
    var config = {
        container_id: "viz",
        server_url: process.env.NEO4J_BOLT,
        server_user: process.env.NEO4J_USERNAME,
        server_password: process.env.NEO4J_PASSWORD,
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
        initial_cypher: "MATCH (n)-[r:INTERACTS]->(m) RETURN * LIMIT 25"
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