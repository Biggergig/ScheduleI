from agents import *
from collections import Counter
from rideTheBus import Game, Card
from tqdm import tqdm
from itertools import permutations


game = Game()


def sim(agent):
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


def treeSearch(agent):
    DECK = [Card(suit, val) for suit in "SHDC" for val in range(1, 14)]

    total_runs = 0
    total_EV = 0
    for chosen in tqdm(permutations(DECK, 4), total=52 * 51 * 50 * 49):
        game.chosen = list(chosen)
        game.cards = list(chosen) + [c for c in DECK if c not in chosen]
        # print(game.chosen, game.cards)

        total_EV += sim(agent)
        total_runs += 1
    return total_EV / total_runs


if __name__ == "__main__":
    agent = StatsAgent(r2Threshold=16, r3Threshold=24)
    # iters = 100000
    # # iters = 1
    # rew_sum = 0
    # counts = Counter()
    # for _ in tqdm(range(iters)):
    #     game.reset()
    #
    #     res = sim(agent)
    #     counts[res] += 1
    #     rew_sum += res
    print(treeSearch(agent))
    # print("EV:", rew_sum / iters)
    # print(counts)
    print()
    # game.printStats()
