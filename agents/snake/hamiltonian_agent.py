import numpy as np
from typing import List, Tuple
from agents.base_agent import BaseAgent
from agents.snake.agent_action import AgentAction

class HamiltonianAgent(BaseAgent):
    def __init__(self, grid_size: int):
        self.grid_size = grid_size
        self.hamiltonian_cycle_1, self.hamiltonian_cycle_2 = self.create_hamiltonian_cycles(self.grid_size)
        print(f"Grid size: {self.grid_size}x{self.grid_size}")
        print(f"Hamiltonian cycle 1 length: {len(self.hamiltonian_cycle_1)}")
        print(f"Hamiltonian cycle 2 length: {len(self.hamiltonian_cycle_2)}")
        print(f"First 10 steps of cycle 1: {self.hamiltonian_cycle_1[:10]}")
        print(f"First 10 steps of cycle 2: {self.hamiltonian_cycle_2[:10]}")
        if not self.verify_hamiltonian_cycle(self.hamiltonian_cycle_1, self.grid_size):
            raise ValueError("Failed to generate a valid Hamiltonian cycle 1")
        if not self.verify_hamiltonian_cycle(self.hamiltonian_cycle_2, self.grid_size):
            raise ValueError("Failed to generate a valid Hamiltonian cycle 2")
        self.current_index = 0
        self.current_cycle = self.hamiltonian_cycle_1

    @property
    def name(self) -> str:
        return "Hamiltonian Agent"

    @property
    def agent_type(self) -> str:
        return "Snake Agent"

    def create_hamiltonian_cycles(self, n: int) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        cycle_1 = []
        for i in range(n):
            if i % 2 == 0:
                cycle_1.extend((i, j) for j in range(n))
            else:
                cycle_1.extend((i, j) for j in range(n - 1, -1, -1))

        # Remove the last element to ensure exactly n^2 elements
        cycle_1 = cycle_1[:n * n]

        cycle_2 = cycle_1[::-1]  # Reverse of cycle_1

        return cycle_1, cycle_2

    def verify_hamiltonian_cycle(self, cycle: List[Tuple[int, int]], n: int) -> bool:
        total_cells = n * n
        if len(cycle) != total_cells:
            print(f"Cycle length {len(cycle)} does not match total cells {total_cells}")
            return False
        if len(set(cycle)) != total_cells:
            print("Cycle contains duplicate cells")
            return False
        for i in range(len(cycle) - 1):
            curr = cycle[i]
            next = cycle[i + 1]
            if abs(curr[0] - next[0]) + abs(curr[1] - next[1]) != 1:
                print(f"Invalid move from {curr} to {next}")
                return False
        # Check if the last move connects back to the first move
        if abs(cycle[-1][0] - cycle[0][0]) + abs(cycle[-1][1] - cycle[0][1]) != 1:
            print(f"Invalid move from {cycle[-1]} to {cycle[0]}")
            return False
        return True

    def get_snake_head_position(self, state: np.ndarray) -> Tuple[int, int]:
        return tuple(np.argwhere(state[:,:,1] == 1)[0])

    def get_next_position(self, current_position: Tuple[int, int]) -> Tuple[int, int]:
        try:
            current_index = self.current_cycle.index(current_position)
            next_index = (current_index + 1) % len(self.current_cycle)
            return self.current_cycle[next_index]
        except ValueError:
            print(f"Current position {current_position} not found in cycle")
            return self.current_cycle[0]

    def get_action(self, state: np.ndarray) -> AgentAction:
        snake_head = self.get_snake_head_position(state)
        next_position = self.get_next_position(snake_head)
        print(f"Current head: {snake_head}, Next position: {next_position}")
        if next_position[0] < snake_head[0]:
            return AgentAction.UP
        elif next_position[0] > snake_head[0]:
            return AgentAction.DOWN
        elif next_position[1] < snake_head[1]:
            return AgentAction.LEFT
        else:
            return AgentAction.RIGHT
