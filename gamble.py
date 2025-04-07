from random import shuffle
from tqdm import tqdm


def suit_to_color(suit):
    return "red" if suit in "HD" else "black"


class Actor:

    def __init__(self, lim=7):
        self.step2val = lim

    def step1(self):
        return "red"

    def step2(self, cards):
        # if cards[0][1] >= self.step2val:
        #     return "lower"
        # return "upper"
        if 5 <= cards[0][1] <= 11:
            return "leave"
        if cards[0][1] <= 7:
            return "upper"
        return "lower"

    def step3(self, cards):
        dist = abs(cards[0][1] - cards[1][1] + 1)
        if dist < 4:
            return "outer"
        if dist > 10:
            return "inner"
        return "leave"

    def step4(self, cards):
        return "D"


def sim(actor):
    cards = [(suit, val) for suit in "SHDC" for val in range(2, 15)]
    shuffle(cards)
    picked_cards = cards[:4]
    val = 1
    if actor.step1() != suit_to_color(cards[0][0]):
        return 0
    else:
        val = 2

    step2 = actor.step2(picked_cards[:1])
    if step2 == "leave":
        return val
    if step2 == "upper" and picked_cards[1][1] <= picked_cards[0][1]:
        return 0
    if step2 == "lower" and picked_cards[1][1] >= picked_cards[0][1]:
        return 0
    val = 3

    step3 = actor.step3(picked_cards[:2])
    lb = min(picked_cards[0][1], picked_cards[1][1])
    ub = max(picked_cards[0][1], picked_cards[1][1])
    if step3 == "leave":
        return val
    if step3 == "inner" and not (lb <= picked_cards[2][1] <= ub):
        return 0
    if step3 == "outer" and (lb <= picked_cards[2][1] <= ub):
        return 0

    step4 = actor.step4(picked_cards[:3])
    if step4 == "leave":
        return val
    if step4 != picked_cards[3][0]:
        return 0
    val = 20

    return val


randActor = Actor()
ITERS = 100000
res = [sim(randActor) for _ in tqdm(range(ITERS))]

print("EV:", sum(res) / len(res))
