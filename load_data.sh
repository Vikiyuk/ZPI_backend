#!/bin/bash
echo "Importing data into MongoDB..."
mongoimport --uri="mongodb://mongo:27017" --db=zpi --collection=predictions --file=/data/predictions.json --jsonArray
mongoimport --uri="mongodb://mongo:27017" --db=zpi --collection=zpi --file=/data/zpi.json --jsonArray
