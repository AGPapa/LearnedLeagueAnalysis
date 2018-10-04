import requests
import sys
import time
from random import random
import os

for l in range (78, 79): #end:78
    ll = str(l)

    rundle_file = open("rundles_ll" + ll + ".txt")
    rundles = rundle_file.read().split("\n")[0:200]
    rundles = filter(None, rundles)
    rundle_file.close()

    for rundle in rundles:

        for d in range(1, 26): #end: 25
            md = str(d)

            day_key = "ll" + ll + "md" + md

            if not os.path.isfile("full_page_data/" + day_key + "r" + rundle + ".html"):

                print("writing " + day_key + "r" + rundle);
                time.sleep(4 + random())
                page = requests.get("https://www.learnedleague.com/match.php?" + ll + "&" + md + "&" + rundle)

                f = open("full_page_data/" + day_key + "r" + rundle + ".html", "w")
                f.write(page.content)
                f.close()
