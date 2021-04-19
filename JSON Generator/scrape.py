from bs4 import BeautifulSoup as bs
import requests
import json
import re
import sys

# Setup
try:
    url = sys.argv[1]
    print(url)
    if url == None or url == "":
        print("Please pass a URL as a command line argument.")
        exit()
    r = requests.get(url)
    page = r.text

    soup = bs(page, features="html5lib")
except:
    print("Failed to connect or retrieve URL from command line. Did you pass a URL?")
    exit()

# Helper methods
def S (selector):
    return soup.select(selector)[0].text

def SS (selector):
    return soup.select(selector)

def fix (str):
    return re.sub(' +', ' ', str.replace(u'\u200b', "").replace(u'\u00a0', " ").replace(u'\n', "")).strip()

try:
    # Scrape
    title = fix(S("body > main > div.contentContainer > div.description > ul > li > pre > span"))
    description = fix(S("body > main > div.contentContainer > div.description > ul > li > div"))

    # Constructors
    tempC1 = SS("body > main > div.contentContainer > div.summary > ul > li > section:nth-child(2) > ul > li > table > tbody > tr > th")
    tempC2 = SS("body > main > div.contentContainer > div.summary > ul > li > section:nth-child(2) > ul > li > table > tbody > tr > td")
    constructors = []
    for i in range(2, len(tempC1)):
        constructors.append([fix(tempC1[i].text), fix(tempC2[i-2].text)])

    # Methods
    c1 = SS("body > main > div.contentContainer > div.summary > ul > li > section:nth-child(3) > ul > li > table .colFirst")
    c2 = SS("body > main > div.contentContainer > div.summary > ul > li > section:nth-child(3) > ul > li > table .colSecond")
    c3 = SS("body > main > div.contentContainer > div.summary > ul > li > section:nth-child(3) > ul > li > table .colLast")
    methods = []

    for i in range(1, len(c1)):
        methods.append([fix(c1[i].text), fix(c2[i].text), fix(c3[i].text)])

    # Fields
    c1 = SS("body > main > div.contentContainer > div.summary > ul > li > section:nth-child(1) > ul > li > table > tbody > tr > td.colFirst")
    c2 = SS("body > main > div.contentContainer > div.summary > ul > li > section:nth-child(1) > ul > li > table > tbody > tr.altColor > th")
    c3 = SS("body > main > div.contentContainer > div.summary > ul > li > section:nth-child(1) > ul > li > table > tbody > tr.altColor > td.colLast")
    fields = []

    for i in range(0, len(c1)):
        fields.append([fix(c1[i].text), fix(c2[i].text), fix(c3[i].text)])

    data = {
        "Title": title,
        "Description": description,
        "Constructors": constructors,
        "Fields": fields,
        "Methods": methods
    }

    with open("website.json", "w") as f:
        json.dump(data, f, indent = 4)

    print("Done, saved to website.json")
except:
    print("There was a problem scraping that URL, was it a javadoc?")

