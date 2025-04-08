from rideTheBus import Card
import simplejson as json

DECK = [Card(suit, val) for suit in "SHDC" for val in range(1, 14)]

cache = {} # state -> (EV, action)

def expectimax(state):
    if state in cache:
        return cache[state][0]

    if len(state) == 3: # choose suit
        choices = set("SHDC")
        for card in state:
            choices.discard(card.suit)
        choice = choices.pop()
        EV = 0
        count = 0
        for c in DECK:
            if c not in state:
                EV += 20 if c.suit == choice else 0
                count += 1
        cache[state] = (EV/count, choice)
        return cache[state][0]

    if len(state) == 2: # inside / outside
        insideEV = 0
        outsideEV = 0
        count = 0
        lb = min(state[0].getValue(), state[1].getValue())
        ub = max(state[0].getValue(), state[1].getValue())
        for c in DECK:
            if c not in state:
                count+=1
                if lb <= c.val <= ub:
                    insideEV += expectimax(state + (c,))
                else:
                    outsideEV += expectimax(state + (c,))
        choices = ["inside", "outside", "forfeit"]
        values = [insideEV/count, outsideEV/count, 3]
        cache[state] = (max(values), choices[values.index(max(values))])
        return cache[state][0]

    if len(state) == 1: # upper / lower
        upperEV = 0
        lowerEV = 0
        count = 0
        for c in DECK:
            if c not in state:
                count+=1
                if c.getValue() > state[0].getValue():
                    upperEV += expectimax(state + (c,))
                elif c.getValue() < state[0].getValue():
                    lowerEV += expectimax(state + (c,))
        choices = ["upper", "lower", "forfeit"]
        values = [upperEV/count, lowerEV/count, 2]
        # print(*zip(choices, values),sep='\n')
        cache[state] = (max(values), choices[values.index(max(values))])
        return cache[state][0]
        
    if len(state) == 0:
        redEV = 0
        blackEV = 0
        count = 0
        for c in DECK:
            if c not in state:
                count+=1
                if c.getColor() == "red":
                    redEV += expectimax(state + (c,))
                elif c.getColor() == "black":
                    blackEV += expectimax(state + (c,))
        choices = ["red", "black", "forfeit"]
        values = [redEV/count, blackEV/count, 1]
        cache[state] = (max(values), choices[values.index(max(values))])
        return cache[state][0]

print("SOLVED EV:",expectimax(()))
print(len(cache))

# cache = {str(k):v for k,v in cache.items()}
# with open("cache.json", "w") as f:
#     json.dump(cache, f, indent=4, sort_keys=True)