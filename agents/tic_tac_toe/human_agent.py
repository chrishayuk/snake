# File: agents/tic_tac_toe/human_agent.py
from agents.agent_type import AgentType
from agents.tic_tac_toe.base_tic_tac_toe_classic_agent import BaseTicTacToeClassicAgent

class HumanAgent(BaseTicTacToeClassicAgent):
    def __init__(self, id: str, name: str, description: str, player=1):
        super().__init__(id, name, description, player)

    @property
    def agent_type(self) -> AgentType:
        return AgentType.HUMAN  # You may need to add a HUMAN type in `AgentType`

    def get_action(self, step: int, state, rendered_state: str, current_player: int) -> int:
        # Show the current state of the game to the human player
        print(rendered_state)
        
        while True:
            try:
                action = int(input(f"Player {current_player} ({'X' if current_player == 1 else 'O'}), select your move (1-9): "))
                if action not in range(1, 10):
                    raise ValueError("Invalid input, select a number between 1 and 9.")
                if self.is_move_valid(state, action):
                    return action
                else:
                    print("Invalid move: Cell is already occupied. Try again.")
            except ValueError as ve:
                print(ve)

    def is_move_valid(self, state, action):
        row, col = self.reverse_action_map[action]
        return state[row, col] == 0
