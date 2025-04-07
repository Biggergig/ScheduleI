import gymnasium as gym
from rideTheBus import Game


class Env(gym.Env):
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.stage = 0
        self.observation_space = gym.spaces.Dict(
            {
                "seen": gym.spaces.Discrete(4),
                "card1": gym.spaces.MultiDiscrete([4, 13]),
                "card2": gym.spaces.MultiDiscrete([4, 13]),
                "card3": gym.spaces.MultiDiscrete([4, 13]),
                "card4": gym.spaces.MultiDiscrete([4, 13]),
            }
        )

        self.action_space = gym.spaces.Discrete(5)

    def _get_obs(self):
        return {
            "seen": self.stage,
            "card1": self.game.chosen[0],
            "card2": self.game.chosen[1],
            "card3": self.game.chosen[2],
            "card4": self.game.chosen[3],
        }

    def _get_info(self):
        return {}

    def reset(self):
        self.game.reset()
        self.stage = 0
        return self._get_obs(), self._get_info()

    def step(self, action):
        # TODO: all of this lmao
        return 0, 0, True, {}
