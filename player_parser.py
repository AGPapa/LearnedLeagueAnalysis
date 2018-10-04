from lxml import html
import sys
from unidecode import unidecode
import re
import json

num_extra_rows = 3
name_col = 7
q_cols = range(0, 6)

ll = "78"
md = "25"

day_key = "ll" + ll + "md" + md

#text = open(day_key + "rA_Metro.html").read()
#sys.stdout.write(text);
#text = text.replace('<I>', '');
#text = text.replace('</I>', '');
#tree = html.fromstring(text)

#path = "//a[text()='Q1']/../../text()"
#q1 = tree.xpath(path)[1]


q_correct_row_path = "//table[@summary='Data table for current LL standings']/tbody/tr"

player_history = {}

for l in range (78, 79): #end:78
    ll = str(l)

    rundle_file = open("rundles_ll" + ll + ".txt")
    rundles = rundle_file.read().split("\n")
    rundles = filter(None, rundles)
    rundle_file.close()

    for rundle in rundles:

        for d in range(1, 26): #end: 25
            md = str(d)

            day_key = "ll" + ll + "md" + md

            text = open("full_page_data/" + day_key + "r" + rundle + ".html").read()

            tree = html.fromstring(text)
            rows = tree.xpath(q_correct_row_path)

            for player_index in range(0, len(rows) - num_extra_rows):
                cols = rows[player_index].xpath("td")

                player_name = cols[name_col].xpath("a/img")[0].get("title")

                for q in q_cols:
                    correct = cols[q].get('class') == "c1"

                    q_key = day_key + "Q" + str(q+1)

                    if player_name in player_history:
                        player_history[player_name][q_key] = correct
                    else:
                        player_history[player_name] = {q_key: correct}

f = open("player_history.json", "w")
f.write(json.dumps(player_history, sort_keys=True, indent=4, separators=(',', ': ')))
f.close()
#""/td"
