neo4j-admin import --nodes:Link="./data/output/nodes/part-00000-1d626f33-5513-4c90-aadc-e7c20972c905-c000.csv"\
    --relationships:SENT_TO="./data/output/relationships/relationship-header.csv,./data/output/relationships/part.*"\
    --id-type STRING \
    --multiline-fields false \
    --ignore-extra-columns true \
    --ignore-missing-nodes true