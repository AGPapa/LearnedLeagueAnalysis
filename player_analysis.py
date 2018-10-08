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

def f(x): # ReLU
    return torch.clamp(x,min=0)
def df(y): # derivative of f composed with inverse of f
    return torch.clamp(torch.sign(y),min=0)


#np.random.seed(100);
#torch.manual_seed(100)
#torch.cuda.manual_seed_all(100)

# Read in the data
player_history = json.loads(open("player_history.json").read());


# Only include players with 600 recorded questions

#player_history_600 = {}

#for player in player_history:
#    if len(player_history[player]) == 600:
#        player_history_600[player] = player_history[player]

#player_history = player_history_600

# Build the matrix
num_questions = 600
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
            max_q_index = max_q_index + 1

        q_ind = q_index_map[question]
        all_data[p_ind][q_ind] = bool2int(player_history[player][question])

    p_ind = p_ind + 1

# Permuting the data

p_perm = torch.randperm(num_players)
all_data = all_data[p_perm]

q_key = "ll78md25Q3"
print("Predicting question:" + q_key)
q_ind = q_index_map[q_key]

# Training

training_percent = 0.75
cutoff = int(training_percent * num_players)

trainlabels = all_data[:cutoff,q_ind] # use last question as label
traininput = torch.cat((all_data[:cutoff,:q_ind], all_data[:cutoff,q_ind+1:]),1) # use first n-1 questions as input

testlabels = all_data[cutoff:,q_ind] # use last question as label
testinput = torch.cat((all_data[cutoff:,:q_ind], all_data[cutoff:,q_ind+1:]),1) # use first n-1 questions as input

# mini-batches

n0 = 599                 # widths of layers
n1 = 18
n2 = 2

eta = 0.01               # learning rate parameter
epsinit = 0.001           # magnitude of initial conditions for synaptic weights
lambd = 0.95              # weight penalty

# one hidden fully connected synaptic layers
W1 = epsinit*torch.randn(n1,n0)
W2 = epsinit*torch.randn(n2,n1)
#biases
b1 = torch.ones(n1, 1)*n0*epsinit
b2 = torch.ones(n2, 1)*n1*epsinit

tmax = 60000             # maximum number of learning updates
tshow = 5000             # how often to pause for visualization
errsq = torch.zeros(tmax)
errcl = torch.zeros(tmax)
errclvalidate = torch.zeros(int(tmax / tshow))

mtotal = num_questions
mvalidate = len(testlabels)
mtrain = len(trainlabels)

batchsize = 32     # minibatch size

for t in range(tmax):
    # generate random samples from train set
    batchindices = [int(np.floor(mtrain * np.random.rand())) for i in range(batchsize)]
    x0 = torch.zeros(n0, batchsize)
    for i, j in zip(range(batchsize), batchindices):
        x0[:, i] = traininput[j]

    #y = -torch.ones(n3, batchsize)
    y = torch.zeros(n2, batchsize)
    for i, j in zip(range(batchsize), batchindices):
        y[int(trainlabels[j]), i] = 1.0

    B1 = b1.repeat(1, batchsize).view(n1, batchsize)
    B2 = b2.repeat(1, batchsize).view(n2, batchsize)

    # forward pass
    x1 = f(torch.mm(W1,x0)+B1)
    x2 = f(torch.mm(W2,x1)+B2)

    # error computation
    errsq[t] = sum(sum(torch.pow((y-x2), 2))) / batchsize
    errcl[t] = sum([float(np.argmax(x2[:, i]) != int(trainlabels[j])) for i, j in zip(range(batchsize), batchindices)]) / batchsize
    delta2 = (y-x2)*df(x2)

    # backward pass
    delta1 = torch.mm(W2.transpose(1,0), delta2)*df(x1)

    # learning updates
    W2 += eta / batchsize * (torch.mm(delta2, x1.transpose(1,0)) - lambd * W2)
    W1 += eta / batchsize * (torch.mm(delta1, x0.transpose(1,0)) - lambd * W1)
    b2 += eta / batchsize * (torch.sum(delta2, dim=1).view(n2, 1) - lambd * b2)
    b1 += eta / batchsize * (torch.sum(delta1, dim=1).view(n1, 1) - lambd * b1)

    if (t + 1) % tshow == 0:    # visualization every tshow steps
        avgerrsq = torch.sum(errsq[: (t + 1)].view(int((t + 1) / tshow), tshow), dim=1).view(int((t + 1) / tshow), 1) / tshow
        avgerrcl = torch.sum(errcl[: (t + 1)].view(int((t + 1) / tshow), tshow), dim=1).view(int((t + 1) / tshow), 1) / tshow

        # compute error on validation set
        x0 = torch.zeros(n0, mvalidate)
        for i in range(mvalidate):
            x0[:, i] = testinput[i].view(n0)
        B1 = b1.repeat(1, mvalidate).view(n1, mvalidate)
        B2 = b2.repeat(1, mvalidate).view(n2, mvalidate)

        x1 = f(torch.mm(W1,x0)+B1)
        x2 = f(torch.mm(W2,x1)+B2)

        errclvalidate[int((t + 1) / tshow - 1)] = sum([float(np.argmax(x2[:, i]) != int(testlabels[i])) for i in range(mvalidate)]) / mvalidate

        print(avgerrsq[int((t + 1) / tshow - 1)], avgerrcl[int((t + 1) / tshow - 1)], errclvalidate[int((t + 1) / tshow - 1)])
