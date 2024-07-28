reflection_prompt_template = """
You have just completed a game of Snake. Reflect on the game to identify areas for improvement.

Strategy:
{strategy}

Game Summary:
{summary}

Strategy Improvement Notes:

Reflect on your performance and suggest improvements for future games.
This must be in the form of prompts and could include examples of good or bad moves.
These should be additions to the strategy to improve the decision-making.
These will be placed with the strategy for future games, so make them super sharp improvements to the strategy to fix errors in this gameplay.
Place the notes to improve the strategy in the strategyImprovementNotes tags.
You should consider these notes as standalone and additive to complement the existing strategy. The agent won't have access to the previous game history, actions or steps, so pure strategy notes.
Keep existing notes that are useful and improve, do not overwrite, blend and improve.
Be specific, give examples of why a move was wrong, using positions and actions to clarify the improvement.  DO NOT refer to steps as agent won't have access to previous history.  Only give standalone examples with coordinates.
Do not lose notes, but can consolidate previous notes into improved strategy improvement notes.

<strategyImprovementNotes>
place notes here
</strategyImprovementNotes>
"""
