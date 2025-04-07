from .baseAgent import Agent


class HandAgent(Agent):
    def round1(self, cards):
        return 0  # always go red

    def round2(self, cards):
        return -1  # forfeit
