var viz;
function draw() {
    var config = {
        container_id: "viz",
        server_url: $("#url").val(),
        server_user: $("#user").val(),
        server_password: $("#pass").val(),
        labels: {},
        relationships: {},
        initial_cypher: $("#cypher").val()
    };
    config.labels["name"] = {
        "caption": $("#caption").val(),
        "size": $("#size").val(),
        "community": $("#community").val(),
    };
    config.relationships[$("#rel_type").val()] = {
        "thickness": $("#thickness").val(),
        "caption": $("#rel_caption").val(),
    }
    viz = new NeoVis.default(config);
    viz.render();
    console.log(viz);
}