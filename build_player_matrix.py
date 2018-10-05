import json
import numpy as np
import torch

def softmax(values):
  max_val = max(values)
  return torch.exp(values - max_val)/torch.sum(torch.exp(values - max_val))

def bool2int(value):
    if value:
        return 1.0
    else:
        return 0.0


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


# Only include players with 450 recorded questions

player_history_450 = {}

for player in player_history:
    if len(player_history[player]) == 450:
        player_history_450[player] = player_history[player]

player_history = player_history_450



# Build the matrix
num_questions = 450
num_players = len(player_history)
all_data = torch.zeros((num_players, num_questions))

q_index_map = {}
q_index_rev_map = {}
max_q_index = 0

p_ind = 0

for player in player_history:
    for question in player_history[player]:
        if question not in q_index_map:
            q_index_map[question] = max_q_index
            q_index_rev_map[max_q_index] = question
            max_q_index = max_q_index + 1

        q_ind = q_index_map[question]
        all_data[p_ind][q_ind] = bool2int(player_history[player][question])

    p_ind = p_ind + 1

# Permuting the data

p_perm = torch.randperm(num_players)
all_data = all_data[p_perm]

q_perm = torch.randperm(num_questions)
all_data = all_data[:,q_perm]
q_index_rev_map_permutation = {}
for i, p in enumerate(q_perm):
    q_index_rev_map_permutation[int(p)] = q_index_rev_map[i]
q_index_rev_map = q_index_rev_map_permutation

print("Predicting question:")
print(q_index_rev_map[num_questions-1])

training_percent = 0.6
cutoff = int(training_percent * num_players)

# Training
tmax = 20000

loss = np.zeros(tmax)     # square error vs. time
errcl = np.zeros(tmax)

trainlabels = all_data[:cutoff,-1] # use last question as label
traininput = all_data[:cutoff,:-1] # use first n-1 questions as input

testlabels = all_data[cutoff:,-1]
testinput = all_data[cutoff:,:-1]

epsinit = 0.01
w = epsinit*torch.rand(num_questions-1)   # random initialization of weight vector
b = epsinit*torch.rand(1)    # random initialization of bias

eta = 0.1

print("Training loss")
for t in range(0, tmax):     # iterate over the train steps
#    i = torch.floor(cutoff*torch.rand(1)).long()    # choose a random example
    x = traininput

    desired = trainlabels  # get true label as a float
    actual = (torch.sum(w*x,1) + b > 0).float()

    delta = desired - actual
    delta = delta.view(-1,1)
    loss[t] = (torch.sum(delta))*(torch.sum(delta))/2.0

    w += eta * torch.sum(delta * x,0)  # weight update
    b += eta * torch.sum(delta)      # bias update

    if t % 1000 == 0:
        x = testinput
        desired = np.float64(testlabels)  # get true label as a float
        actual = np.float64(torch.sum(w*x, 1) + b > 0)
        delta = desired - actual

        print(np.sum(loss[: t + 1])/(t+1), np.average(abs(desired - actual)))

print(np.average(w))


# Testing
x = testinput
desired = np.float64(testlabels)  # get true label as a float
actual = np.float64(torch.sum(w*x, 1) + b > 0)
delta = desired - actual

print("Final Testing Accuracy")
print(1-np.average(abs(desired - actual)))
