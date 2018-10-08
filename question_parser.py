from lxml import html
import sys
from unidecode import unidecode
import re
import json

num_extra_rows = 3
name_col = 7
q_cols = range(1, 7)


q_history = {}

for l in range (75, 79): #end:78
    ll = str(l)

    for d in range(1, 26): #end: 25
        md = str(d)

        day_key = "ll" + ll + "md" + md

        text = open("full_page_data/" + day_key + "rA_Metro.html").read()

        text = text.replace('<I>', '');
        text = text.replace('</I>', '');
        tree = html.fromstring(text)

        path = "//a[text()='Q1']/../../text()"
        q1 = tree.xpath(path)[1]

        for q in q_cols:
            q_key = day_key + "Q" + str(q)

            q_path = "//a[text()='Q" + str(q) + "']/../../text()"
            q_toks = tree.xpath(q_path)[1].split(' - ')

            a_path = "//a[text()='Q" + str(q) + "']/../../span[@class='a-red']"
            a = tree.xpath(a_path)[0].text

            q_history[q_key] = { "C": q_toks[0][1:], "Q": q_toks[1], "A": a }


f = open("question_history.json", "w")
f.write(json.dumps(q_history, sort_keys=True, indent=4, separators=(',', ': ')))
