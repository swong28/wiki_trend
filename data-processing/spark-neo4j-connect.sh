spark-shell --jars neo4j-spark-connector_2.11-full-2.1.0-M4.jar
spark-shell --packages neo4j-contrib:neo4j-spark-connector:2.1.0-M4

spark-shell --conf spark.neo4j.bolt.password=neo4j --packages neo4j-contrib:neo4j-spark-connector:2.2.1-M5

