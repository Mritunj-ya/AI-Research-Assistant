import requests
import xml.etree.ElementTree as ET
url= "https://export.arxiv.org/api/query"
params={
    "search_query":"all:Large Language Models",
    "start":0,
    "max_results":3
}
response=requests.get(url, params=params)
root=ET.fromstring(response.text)

namespace={
    "atom":"http://www.w3.org/2005/Atom"
}
entries=root.findall("atom:entry",namespace)
print(f"Total Papers:{len(entries)}")
first_entry=entries[0]
title=first_entry.find("atom:title",namespace).text
summary=first_entry.find("atom:summary",namespace).text
published=first_entry.find("atom:published",namespace).text
print("Title:",title)
print("Published:",published)
print("Summary:",summary[:300])
