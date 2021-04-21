#!/bin/bash

cd ./bin
python ./scrape.py $1
cd ..

cd ./bin/linux-x64
./AzuriteGenerator
cd ../..