common_strategy = """
Initial Move: Start with random guess as there is no prior information.
Use Feedback: Use feedback ("North", "South", "East", "West") to narrow down the location of the treasure.
Minimize Overlap: Avoid guessing previously guessed cells to maximize the coverage of the grid.
Decision-Making Process:

Analyze the current state to identify guessed cells.
Use the feedback from previous guesses to determine the most likely location of the treasure.
Make a decision that aligns with the strategy to maximize the chance of finding the treasure with minimal guesses.
"""