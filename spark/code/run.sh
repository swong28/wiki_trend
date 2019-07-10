aws s3 sync s3://modified-clickstream-data/output ./data

sudo rm -rf /etc/neo4j/data/databases/

sudo neo4j-admin import --nodes:Link="./data/output/node/part-00000-85e73bdb-3a19-4033-8fb3-a55584a5e2f1-c000.csv"\
    --relationships:SENT_TO="./data/output/relationship/relationship-header.csv,./data/output/relationship/part.*"\
    --id-type STRING \
    --multiline-fields false \
    --ignore-extra-columns true \
    --ignore-missing-nodes true