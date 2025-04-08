from random import shuffle
from tqdm import tqdm
import concurrent.futures

def suit_to_color(suit):
    return "red" if suit in "HD" else "black"

class Actor:
    def __init__(self, lim=7):
        self.step2val = lim

    def step1(self):
        return "red"

    def step2(self, cards, step1cutoff):
        middle = 8
        lb = middle - step1cutoff
        ub = middle + step1cutoff
        if lb <= cards[0][1] <= ub:
            return "leave"
        if cards[0][1] <= middle:
            return "upper"
        return "lower"
    
    def step3(self, cards, step2cutoff):
        dist = abs(cards[0][1] - cards[1][1] + 1)
        middle = 6
        lb = middle - step2cutoff
        ub = middle + step2cutoff
        if dist < lb:
            return "outer"
        if dist > ub:
            return "inner"
        return "leave"

    def step4(self, cards):
        selected_suits = {suit for suit, _ in cards}
        remaining_suits = {"S", "H", "D", "C"} - selected_suits
        return remaining_suits.pop()
        

def sim(actor, step1cutoff, step2cutoff, ITERS):
    res = []
    for _ in range(ITERS):
        cards = [(suit, val) for suit in "SHDC" for val in range(2, 15)]
        shuffle(cards)
        picked_cards = cards[:4]
        val = 1
        if actor.step1() != suit_to_color(cards[0][0]):
            res.append(0)
            continue
        else:
            val = 2

        step2 = actor.step2(picked_cards[:1], step1cutoff)
        if step2 == "leave":
            res.append(val)
            continue
        if step2 == "upper" and picked_cards[1][1] <= picked_cards[0][1]:
            res.append(0)
            continue
        if step2 == "lower" and picked_cards[1][1] >= picked_cards[0][1]:
            res.append(0)
            continue
        val = 3

        step3 = actor.step3(picked_cards[:2], step2cutoff)
        lb = min(picked_cards[0][1], picked_cards[1][1])
        ub = max(picked_cards[0][1], picked_cards[1][1])
        if step3 == "leave":
            res.append(val)
            continue
        if step3 == "inner" and not (lb <= picked_cards[2][1] <= ub):
            res.append(0)
            continue
        if step3 == "outer" and (lb <= picked_cards[2][1] <= ub):
            res.append(0)
            continue

        step4 = actor.step4(picked_cards[0:3])
        if step4 == "leave":
            res.append(val)
            continue
        if step4 != picked_cards[3][0]:
            res.append(0)
            continue
        val = 20

        res.append(val)
    # Calculate EV for this set of iterations
    ev = sum(res) / len(res)
    return (step1cutoff, step2cutoff, ev)

if __name__ == "__main__":
    ITERS = 100000
    max_ev = 0
    max_step1 = 0
    max_step2 = 0
    results = []

    # Setting max_workers=36 to attempt to run all cases concurrently
    with concurrent.futures.ProcessPoolExecutor(max_workers=36) as executor:
        futures = []
        for i in range(0, 7):
            for j in range(0, 7):
                print(f"Submitting simulation for step1cutoff: {i} step2cutoff: {j}")
                # Create a new Actor instance in each process
                actor = Actor()
                futures.append(executor.submit(sim, actor, i, j, ITERS))
        for future in concurrent.futures.as_completed(futures):
            step1, step2, ev = future.result()
            print(f"For step1cutoff: {step1} and step2cutoff: {step2} EV is: {ev}")
            if ev > max_ev:
                max_ev = ev
                max_step1 = step1
                max_step2 = step2

    print("Max EV:", max_ev)
    print("Max step1:", max_step1)
    print("Max step2:", max_step2)