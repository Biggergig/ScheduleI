from agents import *
from collections import Counter
from rideTheBus import Game
from tqdm import tqdm


game = Game()


def sim(agent):
    game.reset()
    EV = 1
    act1 = agent.round1(game.chosen[:0])
    newEV = game.round1(act1)
    if newEV == EV:
        return EV
    if newEV == 0:
        return 0
    EV = newEV

    act2 = agent.round2(game.chosen[:1])
    newEV = game.round2(act2)
    if newEV == EV:
        return EV
    if newEV == 0:
        return 0
    EV = newEV

    act3 = agent.round3(game.chosen[:2])
    newEV = game.round3(act3)
    if newEV == EV:
        return EV
    if newEV == 0:
        return 0
    EV = newEV

    act4 = agent.round4(game.chosen[:3])
    newEV = game.round4(act4)
    if newEV == EV:
        return EV
    if newEV == 0:
        return 0
    EV = newEV
    return EV


if __name__ == "__main__":
    agent = StatsAgent(r2Threshold=16)
    iters = 100000
    # iters = 1
    rew_sum = 0
    counts = Counter()
    for _ in tqdm(range(iters)):
        res = sim(agent)
        counts[res] += 1
        rew_sum += res
    print("EV:", rew_sum / iters)
    print(counts)
