# wiki_trend

USING PERIODIC COMMIT 
LOAD CSV FROM 'https://modified-clickstream-data.s3.amazonaws.com/part-00029-0f06face-ba40-4b4e-a2ba-d861e2902f93-c000.csv' AS line
MERGE (n1:Link {name: line[0]})
MERGE (n2:Link {name: line[2]})
MERGE (n1) -[r:SENT_TO {occurence: line[1]}]->(n2)