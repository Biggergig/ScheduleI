from dataclasses import dataclass
from random import shuffle
from tabulate import tabulate

SUIT_TO_ICON = {
    "S": "♠",
    "H": "♥",
    "D": "♦",
    "C": "♣",
}

VALUE_TO_ICON = {
    1: "A",
    11: "J",
    12: "Q",
    13: "K",
}


@dataclass
class Card:
    suit: str
    val: int

    def __repr__(self):
        return f"{VALUE_TO_ICON.get(self.val, self.val)}{SUIT_TO_ICON[self.suit]}"

    def getColor(self):
        return "red" if self.suit in "HD" else "black"

    def getValue(self):
        return self.val if self.val != 1 else 14


class Game:
    def __init__(self):
        self.cards = [Card(suit, val) for suit in "SHDC" for val in range(1, 14)]
        self.chosen = []
        self.correct_counts = [0, 0, 0, 0]
        self.total_counts = [0, 0, 0, 0]
        self.reset()

    def reset(self):
        shuffle(self.cards)
        # self.correct_counts = [0, 0, 0, 0]
        # self.total_counts = [0, 0, 0, 0]
        self.chosen = self.cards[:4]

    def round1(self, action):
        if action == -1:  # forfeit
            return 1
        self.total_counts[0] += 1
        if action == 0 and self.chosen[0].getColor() == "red":  # red
            self.correct_counts[0] += 1
            return 2
        if action == 1 and self.chosen[0].getColor() == "black":  # black
            self.correct_counts[0] += 1
            return 2
        return 0  # bust

    def round2(self, action):
        if action == -1:  # forfeit
            return 2
        self.total_counts[1] += 1
        if (
            action == 0 and self.cards[1].getValue() < self.chosen[0].getValue()
        ):  # lower
            self.correct_counts[1] += 1
            return 3
        if (
            action == 1 and self.cards[1].getValue() > self.chosen[0].getValue()
        ):  # upper
            self.correct_counts[1] += 1
            return 3
        return 0  # bust

    def round3(self, action):
        if action == -1:  # forfeit
            return 3
        self.total_counts[2] += 1
        lb = min(self.chosen[0].getValue(), self.cards[1].getValue())
        ub = max(self.chosen[0].getValue(), self.cards[1].getValue())
        if action == 0 and lb <= self.cards[2].getValue() <= ub:  # inner
            self.correct_counts[2] += 1
            return 4
        if action == 1 and not (lb <= self.cards[2].getValue() <= ub):  # outer
            self.correct_counts[2] += 1
            return 4
        return 0  # bust

    def round4(self, action):
        if action == -1:  # forfeit
            return 4
        self.total_counts[3] += 1
        suit = "SHDC"[action]
        # print(self.chosen, suit)
        if self.cards[3].suit == suit:  # same color
            # print("MATCH")
            self.correct_counts[3] += 1
            return 20
        return 0  # bust

    def play(self):
        self.reset()
        EV = 1
        act = int(input("(-1) forfeit, (0) red, (1) black\n"))
        print(self.chosen[:1])
        newEV = self.round1(act)
        if newEV == EV:
            print("Left with", newEV)
            return
        if newEV == 0:
            print("Bust!")
            return
        EV = newEV

        act = int(input("(-1) forfeit, (0) lower, (1) upper\n"))
        print(self.chosen[:2])
        newEV = self.round2(act)
        if newEV == EV:
            print("Left with", newEV)
            return
        if newEV == 0:
            print("Bust!")
            return
        EV = newEV

        act = int(input("(-1) forfeit, (0) inner, (1) outer\n"))
        print(self.chosen[:3])
        newEV = self.round3(act)
        if newEV == EV:
            print("Left with", newEV)
            return
        if newEV == 0:
            print("Bust!")
            return
        EV = newEV

        act = int(input("(-1) forfeit, (0) S, (1) H, (2) D, (3) C\n"))
        print(self.chosen[:4])
        newEV = self.round4(act)
        if newEV == EV:
            print("Left with", newEV)
            return
        if newEV == 0:
            print("Bust!")
            return
        EV = newEV
        print("recieved EV:", EV)

    def printStats(self):
        data = [
            ["Round 1", "Round 2", "Round 3", "Round 4"],
            self.correct_counts,
            self.total_counts,
            [self.correct_counts[i] / self.total_counts[i] for i in range(4)],
        ]

        print(
            tabulate([*zip(*data)], headers=["Round", "Correct", "Total", "Percentage"])
        )


if __name__ == "__main__":
    game = Game()
    game.play()
