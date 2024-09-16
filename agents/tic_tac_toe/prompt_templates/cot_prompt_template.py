cot_prompt_template = """
You are an AI playing Tic Tac Toe. You are playing as {player}.

Current Game State:
{state}

<agentThinking>
**Explain your thought process, considering:**
1. **Your mark on the board** (X or O depending on which player you are).
2. **The current state of the board** (which spaces are taken, which are empty).
3. **Potential winning opportunities** (evaluate if you can win in the next move).
4. **Blocking opponent opportunities** (consider if your opponent is about to win, and how you can block them).
5. **Strategic moves** (assess the best move based on an overall strategy, such as controlling the center or creating a fork).
6. **Final choice** (explain why the move you choose maximizes your chance of winning or prevents a loss).
</agentThinking>

Provide your final decision as a single number from 1 to 9 in a `finalOutput` tag, representing the cell you choose to place your mark. For example:
<finalOutput>
final decision goes here
</finalOutput>

"""