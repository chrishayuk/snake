# File: agents/snake/smart_seeker_agent.py
import time
from agents.snake.agent_action import AgentAction
from agents.snake.classic_agent import ClassicAgent

class SmartSeekerAgent(ClassicAgent):
    def get_action(self, state) -> AgentAction:
        # Check if the state is a string or numpy array
        if isinstance(state, str):
            state = self.parse_state_string(state)

        # get the position of the snake head
        snake_head = self.get_snake_head_position(state)

        # get the food position
        food = self.get_food_position(state)

        # get the snake body positions
        snake_body = self.get_snake_body_positions(state)

        # Define the possible moves
        possible_moves = {
            AgentAction.UP: (snake_head[0] - 1, snake_head[1]),
            AgentAction.DOWN: (snake_head[0] + 1, snake_head[1]),
            AgentAction.LEFT: (snake_head[0], snake_head[1] - 1),
            AgentAction.RIGHT: (snake_head[0], snake_head[1] + 1),
        }

        # Define the opposite directions
        opposite_directions = {
            AgentAction.UP: AgentAction.DOWN,
            AgentAction.DOWN: AgentAction.UP,
            AgentAction.LEFT: AgentAction.RIGHT,
            AgentAction.RIGHT: AgentAction.LEFT,
        }

        # Filter out moves that would result in a collision with the snake's body or are opposite to current direction
        safe_moves = {
            action: pos for action, pos in possible_moves.items()
            if pos not in snake_body.tolist() and action != opposite_directions[self.current_direction]
        }

        # Determine the best move that gets closer to the food
        best_move = None
        min_distance = float('inf')
        
        for action, pos in safe_moves.items():
            distance = abs(food[0] - pos[0]) + abs(food[1] - pos[1])
            if distance < min_distance:
                min_distance = distance
                best_move = action

        # If no safe move is found, default to the first safe move
        if best_move is None:
            best_move = next(iter(safe_moves.keys()), AgentAction.UP)

        # set the time completed
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')

        # Update the current direction
        self.current_direction = best_move

        # log the state, thought process, and decision
        self.logger.log_decision(self.game_id, state, "", best_move, best_move, time_completed)

        return best_move
    