# File: environments/tic_tac_toe/reward_functions.py
def simple_reward(won=False, draw=False, ongoing=True):
    """
    Reward function for Tic-Tac-Toe.
    - won: Whether the current player won the game.
    - draw: Whether the game ended in a draw.
    - ongoing: Whether the game is still ongoing.
    """
    if won:
        # Win gives 1 point
        return 1  
    elif draw:
        # Draw gives 0.5 points
        return 0.5  
    elif ongoing:
        # Ongoing games give no reward
        return 0  
    
    # Loss gives negative reward
    return -1  
