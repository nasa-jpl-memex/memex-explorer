#!/bin/bash

source activate memex
echo "memex activated"
elasticsearch &
ES_PID=$!
echo "elasticsearch launched with pid: $ES_PID"
elasticdump --bulk=true --input=elasticdump.json --output=http://localhost:9200/
echo "elasticdump to localhost:9200 complete!"
kill $ES_PID
echo "elasticsearch with pid: $ES_PID has been killed"
