from lxml import html
import requests
import sys
from unidecode import unidecode
import json
import time
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


f = open("q_history.json")
json_data=f.read()
f.close()
#q_history = json.loads(json_data)

q_history = {}

for l in range (76, 77): #end:77
    ll = str(l)
    
    if (ll in q_history.keys()):
        continue
    
    q_history[ll] = {}
    for d in range(7, 8): #end: 25
        md = str(d)
    
        q_history[ll][md] = {}
        
        page = requests.get("https://www.learnedleague.com/match.php?" + ll + "&" + md + "&A_Metro")
        sys.stdout.write(page.content)
        tree = html.fromstring(page.content)
        time.sleep(1)
        
        for q in range (1, 7):
            qu = str(q)
        
            q_history[ll][md][qu] = {}
        
            code = "LL" + ll + "MD" + md + "Q" + qu

            path = "//a[text()='Q" + qu + "']/../../text()"
            
            resp = tree.xpath(path)[1]
            tokens = resp.split(" - ")
            category = unidecode(tokens[0]).strip()
            question = resp
            
            q_history[ll][md][qu]["C"] = category
            q_history[ll][md][qu]["Q"] = question
            
            
#sys.stdout.write(json.dumps(q_history))
f = open("q_history.json", "w")
f.write(json.dumps(q_history, sort_keys=True, indent=4, separators=(',', ': '))) 