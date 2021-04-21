#!/bin/bash

# Run the web scraper from bin
cd ./bin
python ./scrape.py $1

./linux-x64/AzuriteGenerator test
cd ..