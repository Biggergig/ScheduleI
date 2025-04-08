from .baseAgent import Agent
from rideTheBus import Card


class StatsAgent(Agent):
    def __init__(self, r2Threshold=4, r3Threshold=4):
        self.r2Threshold = r2Threshold
        self.r3Threshold = r3Threshold

    def round1(self, cards):
        return 0  # always go red

    def round2(self, cards):
        remaining = [Card(suit, val) for suit in "SHDC" for val in range(1, 14)]
        remaining = [c for c in remaining if c not in cards]
        count = 0
        for c in remaining:
            if c.getValue() > cards[0].getValue():
                count += 1
            if c.getValue() < cards[0].getValue():
                count -= 1
        if count > self.r2Threshold:
            return 1
        elif count < -self.r2Threshold:
            return 0
        else:  # if we see an 8
            return -1  # forfeit

    def round3(self, cards):
        # return -1
        remaining = [Card(suit, val) for suit in "SHDC" for val in range(1, 14)]
        remaining = [c for c in remaining if c not in cards]
        count = 0
        lb = min(cards[0].getValue(), cards[1].getValue())
        ub = max(cards[0].getValue(), cards[1].getValue())
        for c in remaining:
            if lb <= c.getValue() <= ub:
                count += 1
            else:
                count -= 1
        # print(cards, count)
        if count > self.r3Threshold:
            return 0
        elif count < -self.r3Threshold:
            return 1
        else:
            return -1  # forfeit

    def round4(self, cards):
        return -1
        choices = set("SHDC")
        for c in cards:
            choices.discard(c.suit)
        return "SHDC".index(choices.pop())
