from enum import Enum

from algorithms.Algorithm import Algorithm
from algorithms.hill_climbing.BestChoiceHillClimbing import BestChoiceHillClimbing
from algorithms.hill_climbing.FirstChoiceHillClimbing import FirstChoiceHillClimbing
from algorithms.hill_climbing.RandomChoiceHillClimbing import RandomChoiceHillClimbing
from algorithms.simulated_annealing.SimulatedAnnealing import SimulatedAnnealing
from algorithms.tabu_search.TabuSearch import TabuSearch
# from algorithms.genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm


class AvailableAlgorithms(str, Enum):
    BEST_CHOICE_HILL_CLIMBING = "BestChoiceHillClimbing"  # ruff: noqa  BestChoiceHillClimbing.__name__
    FIRST_CHOICE_HILL_CLIMBING = "FirstChoiceHillClimbing"  # ruff: noqa  FirstChoiceHillClimbing.__name__
    RANDOM_CHOICE_HILL_CLIMBING = "RandomChoiceHillClimbing"  # ruff: noqa  RandomChoiceHillClimbing.__name__
    SIMULATED_ANNEALING = "SimulatedAnnealing"  # ruff: noqa  SimulatedAnnealing.__name__
    TABU_SEARCH = "TabuSearch"  # ruff: noqa  TabuSearch.__name__
    # GENETIC_ALGORITHM = "GeneticAlgorithm"  # ruff: noqa  GeneticAlgorithm.__name__

    @classmethod
    def get_algorithm(cls, algorithm: "AvailableAlgorithms") -> Algorithm:
        match algorithm:
            case AvailableAlgorithms.FIRST_CHOICE_HILL_CLIMBING:
                return FirstChoiceHillClimbing
            case AvailableAlgorithms.BEST_CHOICE_HILL_CLIMBING:
                return BestChoiceHillClimbing
            case AvailableAlgorithms.RANDOM_CHOICE_HILL_CLIMBING:
                return RandomChoiceHillClimbing
            case AvailableAlgorithms.SIMULATED_ANNEALING:
                return SimulatedAnnealing
            case AvailableAlgorithms.TABU_SEARCH:
                return TabuSearch
            # case AvailableAlgorithms.GENETIC_ALGORITHM:
            #     return GeneticAlgorithm
            case _:
                raise ValueError(f"Unknown algorithm: {algorithm}")
