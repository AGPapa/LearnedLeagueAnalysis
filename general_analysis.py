import json


# Read in the data
player_history = json.loads(open("player_history.json").read());


bins = {}
for player in player_history:
    q_count = 0
    for question in player_history[player]:
        q_count = q_count + 1
    if q_count in bins:
        bins[q_count] = bins[q_count] + 1
    else:
        bins[q_count] = 1

print("Players by question count:")
print(bins)



question_history = json.loads(open("question_history.json").read());

bins = {}
for question in question_history:
    cat = question_history[question]["C"]
    if cat in bins:
        bins[cat] = bins[cat] + 1
    else:
        bins[cat] = 1

print("Questions by category count:")
print(bins)
