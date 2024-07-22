# Introduction

## Snake
The following will allow you to watch a very simple agent play the game of snake.
To run the game, you can just enter the following command in the command line

```bash
python main_simple.py --env snake
```

This will run a game of snake, where the agent will follow a simple policy of just trying to get to the food as quickly as possible.  There is no AI learning in this game.

### LLM Agents
Snake currently supports a whole bunch of LLM's but pretty much all of them are useless at playing snake.  The following allows you to play using ollama and gemma2 9b.

```bash
python main_simple.py play --env snake --agent snake_gemma2_9b
```

The only model any good at playing snake is gpt-4o

```bash
python main_simple.py play --env snake --agent snake_gpt4o
```
