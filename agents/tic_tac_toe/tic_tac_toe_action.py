# File: agents/tic_tac_toe/tictactoe_action.py
from enum import Enum

class TicTacToeAction(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    @staticmethod
    def from_number(number: int):
        """Utility function to get the TicTacToeAction from a number (1-9)."""
        return TicTacToeAction(number)
