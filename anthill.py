import numpy as np
import random 
import matplotlib.pyplot as plt

P = np.array([[0, 1, 0, 0], [.25, 0, .5, .25], [0, .5, 0, .5], [0, 0, 0, 1]])

def main():
    dist = []
    for i in range(0, 500):
        dist.append(sample())
    plt.hist(dist)
    plt.show()

def sample(n=1000):
    trials = 0
    Sn = 0
    while trials < n:
        Sn += simulate()
        trials += 1
    return Sn/n

def step(i , P ):
    next_states = np.where(P[i,:] > 0)[0]
    state_dist = P[i,:][next_states]
    cumul = np.cumsum(state_dist)
    rand = random.uniform(0,1)
    for i in range(0,len(next_states)):
        if rand <= cumul[i]:
            return next_states[i]

def simulate():
    count = 0
    state = 0
    while state != 3:
        newState = step(state, P)
        count += 1
        state = newState
    return count

main()