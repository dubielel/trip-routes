import logging

import numpy as np
from random import shuffle, randrange
from copy import deepcopy
from sortedcontainers import SortedKeyList

from algorithms.Algorithm import Algorithm
from algorithms.AlgorithmStatistics import AlgorithmStatistics
from algorithms.TripProblem import TripProblem
from algorithms.TripState import TripState

logger = logging.getLogger(__name__)


class GeneticAlgorithm(Algorithm):
    SELECTION_SIZE = 10
    ELITISM_SIZE = 2
    CROSSOVER_FIXED_RATIO = 0.5
    """
    Fraction of the individual genomes that are fixed in the crossover operation
    """

    POPULATION_SIZE = 100
    population: SortedKeyList[TripState]

    def __init__(
        self,
        problem: TripProblem,
        algorithm_statistics: AlgorithmStatistics,
    ):
        self.population = self._init_random_population()

        super().__init__(problem, algorithm_statistics)

    def next_state(self) -> TripState | None:
        """
        Move to the next state based on the current state
        """
        return None

    def _find_next_state(self) -> TripState | None:
        """
        Find the next state based on the current state
        """
        return None

    def _init_random_population(self) -> list[TripState]:
        population = SortedKeyList(key=lambda x: x[1])
        for _ in range(self.POPULATION_SIZE):
            random_state = self.problem.random_state()
            random_state_value = self.problem.evaluate(random_state)
            population.add((random_state, random_state_value))

    # TODO implement
    # - selection -> Steady-State Selection, Tournament Selection, Roulette Wheel Selection?
    # - elitism?
    # - crossover -> Order Crossover (OX1), Order-Based Crossover (OX2), Position-Based Crossover (POS)
    # - mutation -> this is move_method

    def steady_state_selection(self) -> list[tuple[TripState, TripState]]:
        """
        In every generation few individuals are selected (good - with high fitness)
        for creating a new offspring.

        Then some (bad - with low fitness) individuals are removed
        and the new offspring is placed in their place.

        The rest of population survives to new generation.
        """

        # Selection methods should only select individuals from the current population and return them in pairs
        # Crossover methods should not be invoked here

        selected_individuals = self.population[: self.SELECTION_SIZE]

        selected_individuals_indices = list(range(self.SELECTION_SIZE))
        shuffle(selected_individuals_indices)

        random_pairs: list[tuple[TripState, TripState]] = []
        for i in range(0, len(selected_individuals_indices), 2):
            random_pairs.append((selected_individuals[i], selected_individuals[i + 1]))

        return random_pairs

    def tournament_selection(self) -> list[tuple[TripState, TripState]]:
        raise NotImplementedError

    def roulette_wheel_selection(self) -> list[tuple[TripState, TripState]]:
        raise NotImplementedError

    def order_crossover(
        self, parent1: TripState, parent2: TripState
    ) -> tuple[TripState, TripState]:
        # Copy routes without accommodation at the beginning and end
        parent1_route = deepcopy(parent1.route[1:-1])
        parent2_route = deepcopy(parent2.route[1:-1])

        # Replace accommodation with negative values to differentiate them during crossover
        negative_acc = -1
        for i in range(len(parent1_route)):
            if parent1_route[i] == 0:
                parent1_route[i] = negative_acc
                negative_acc -= 1
        negative_acc = -1
        for i in range(len(parent2_route)):
            if parent2_route[i] == 0:
                parent2_route[i] = negative_acc
                negative_acc -= 1

        state_route_length = len(parent1_route)
        fixed_part_size = round(state_route_length * self.CROSSOVER_FIXED_RATIO)
        fixed_part_start = randrange(
            0, state_route_length - fixed_part_size + 1
        )  # inclusive
        fixed_part_end = fixed_part_start + fixed_part_size  # exclusive

        child1 = np.empty(state_route_length, dtype=int)
        child2 = np.empty(state_route_length, dtype=int)

        parent1_fixed_part = parent1_route[fixed_part_start:fixed_part_end]
        parent2_fixed_part = parent2_route[fixed_part_start:fixed_part_end]

        child1[fixed_part_start:fixed_part_end] = parent1_fixed_part
        child2[fixed_part_start:fixed_part_end] = parent2_fixed_part

        parent1_complement = deepcopy(parent1.route)
        parent2_complement = deepcopy(parent2.route)

        for el in parent1_fixed_part:
            parent2_complement.remove(el)

        parent2_complement = (
            parent2.route[fixed_part_end:] + parent2.route[:fixed_part_start]
        )
        raise NotImplementedError

    def order_based_crossover(
        self, parent1: TripState, parent2: TripState
    ) -> tuple[TripState, TripState]:
        raise NotImplementedError

    def position_based_crossover(
        self, parent1: TripState, parent2: TripState
    ) -> tuple[TripState, TripState]:
        raise NotImplementedError
