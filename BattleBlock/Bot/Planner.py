# -*- coding: utf-8 -*-
# Python3.4*

from Bot.Strategies.RandomStrategy import RandomStrategy
from Bot.Strategies.GeneticStrategy import GeneticStrategy
#from Bot.Strategies.RLStrategy import RLStrategy
from Bot.Strategies.HeightStrategy import HeightStrategy


def create(strategyType, game):
    switcher = {
        "random": RandomStrategy(game),
        "genetic": GeneticStrategy(game),
        #"reinforcement": RLStrategy(game),
        "height": HeightStrategy(game)
    }

    strategy = switcher.get(strategyType.lower())

    return Planner(strategy)


class Planner:
    def __init__(self, strategy):
        self._strategy = strategy

    def makeMove(self):
        return self._strategy.choose()
