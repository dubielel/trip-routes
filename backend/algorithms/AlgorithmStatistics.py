class AlgorithmStatistics:
    def __init__(self):
        pass

    # def __init__(self):
    #     self.steps: int = 0
    #     self.time: float = 0.0
    #     self.objective_values: list[float] = []
    #     self.best_objective_values: list[float] = []
    #     self.best_objective_value: float = float("inf")
    #     self.best_objective_value_index: int = 0
    #     self.best_states: list[TripState] = []
    #     self.best_state: TripState | None = None
    #     self.best_state_index: int = 0

    # def update(self, state: TripState, objective_value: float):
    #     self.steps += 1
    #     self.objective_values.append(objective_value)
    #     self.best_objective_values.append(self.best_objective_value)

    #     if objective_value < self.best_objective_value:
    #         self.best_objective_value = objective_value
    #         self.best_state = state
    #         self.best_state_index = self.steps
    #         self.best_states.append(state)
    #     else:
    #         self.best_states.append(self.best_state)

    # def __str__(self):
    #     return f"Steps: {self.steps}, Time: {self.time}, Best objective value: {self.best_objective_value}, Best state: {self.best_state}, Best state index: {self.best_state_index}"
