@echo off

python scrape.py %1

AzuriteGenerator %2
PAUSE
