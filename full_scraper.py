import requests
import sys
import time
from random import random
import os

already_scraped_file = open("scraped_pages.txt")
already_scraped =  already_scraped_file.read().split("\n")
already_scraped =  filter(None, already_scraped)
already_scraped_file.close()


for l in range (75, 79): #end:78
    ll = str(l)

    rundle_file = open("rundles_ll" + ll + ".txt")
    rundles = rundle_file.read().split("\n")[0:250]
    rundles = filter(None, rundles)
    rundle_file.close()

    for rundle in rundles:

        for d in range(1, 26): #end: 25
            md = str(d)

            day_key = "ll" + ll + "md" + md

            filename = day_key + "r" + rundle + ".html"
            if (filename not in already_scraped) and (not os.path.isfile("full_page_data/" + filename)):

                print("writing " + day_key + "r" + rundle);
                time.sleep(4 + random())
                page = requests.get("https://www.learnedleague.com/match.php?" + ll + "&" + md + "&" + rundle)

                f = open("full_page_data/" + day_key + "r" + rundle + ".html", "w")
                f.write(page.content)
                f.close()
