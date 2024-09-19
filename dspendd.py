import random
import math
import sys

# Wouldnt it be nice for graders to see your explaination of what craziness you are doing???
def satoshi(q,z):
    """
    Calculate the probability of a successful doublespend attack using Satoshi's equation.
    
    :param q: Attacker's fraction of the network hash power
    :param z: Number of confirmation blocks
    :return: Probability of attacker's success
    """
    p = 1 - q
    lambda_val = z * q / p
    
    sum_prob = 0
    for k in range(z + 1):
        poisson_prob = ((lambda_val ** k )* math.exp(-lambda_val)) / math.factorial(k)
        geom_prob = 1 - (q / p) ** (z - k)
        sum_prob += (poisson_prob * geom_prob)
    
    return 1 - sum_prob


MAX_LEAD = 35

def simulate_doublespend(q, z):
    """
    Simulate a single instance of the doublespend attack.
    
    :param q: Attacker's fraction of the network hash power
    :param z: Number of confirmation blocks
    :return: True if attacker succeeds, False otherwise
    """
    honest_chain = 0
    attacker_chain = 0
    
    while True:
        if random.random() <= q:
            attacker_chain += 1
        else:
            honest_chain += 1
        
        if honest_chain >= z:
            if attacker_chain > honest_chain:
                return True
            elif honest_chain - attacker_chain >= MAX_LEAD:
                return False
        
        if attacker_chain > honest_chain and attacker_chain > z:
            return True

def monteCarlo(q, z, numTrials=50000):
    """
    Perform Monte Carlo simulation to estimate the probability of a successful doublespend attack.
    
    :param q: Attacker's fraction of the network hash power
    :param z: Number of confirmation blocks
    :param numTrials: Number of simulation trials
    :return: Estimated probability of attacker's success
    """
    successful_attacks = sum(simulate_doublespend(q, z) for _ in range(numTrials))
    return successful_attacks / numTrials

def Test():
    sys.setrecursionlimit(5000)
    q = 0.3

    for z in range(0, 11):
        s = satoshi(q, z)
        mc = monteCarlo(q, z, 10000)
        print("q:", q, " z:", z, " satoshi: %3.3f" % (s*100), " monte carlo: %3.3f" % (mc*100))