from collections import defaultdict
from json import load

with open("solved.json", "r") as f:
    solved = load(f)

choices = defaultdict(set)
for k,v in solved.items():
    cards=k[1:-1].split(", ")
    if len(cards) != 2: continue
    to_val = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":11,"Q":12,"K":13,"A":14}
    v1 = to_val[cards[0][:-1]]
    v2 = to_val[cards[1][:-1]]
    diff = max(v1,v2)-min(v1,v2)
    choices[diff].add(v[1])
    if diff in (5,):
        print(k,diff,v)

print(choices)