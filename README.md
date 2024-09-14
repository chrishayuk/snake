# Introduction

## Environments
This section describes the environments currently supported by the agents.
This is currently limited to 2 environments

- snake
- minesweeper

if you wish to look at the supported environments, this can be supported in the cli,.

```bash
python main_simple.py list-environments
```

### Snake
The following will allow you to watch a very simple agent play the game of snake.
To run the game, you can just enter the following command in the command line

```bash
python main_simple.py play --env snake --agent snake_smart_seeker
```

This will run a game of snake, where the agent will follow a simple policy of just trying to get to the food as quickly as possible.  There is no AI learning in this game.

#### LLM Agents
Snake currently supports a whole bunch of LLM's but pretty much all of them are useless at playing snake.  The following allows you to play using ollama and gemma2 9b.

##### Basic LLM Agent
This following will run a basic llm agent 

```bash
python main_simple.py play --env snake --agent snake_llm --provider ollama --model gemma2:9b
```

The only model any good at playing snake is gpt-4o

```bash
python main_simple.py play --env snake --agent snake_gpt4o --provider openai --model gpt-4o
```

### Minesweeper
The following will allow you to watch a very simple agent play the game of minesweeper.
To run the game, you can just enter the following command in the command line

```bash
python main_simple.py play --env minesweeper --agent minesweeper_test
```

This will run a game of snake, where the agent will follow a simple policy of just trying to get to the food as quickly as possible.  There is no AI learning in this game.

#### LLM Agents
Snake currently supports a whole bunch of LLM's but pretty much all of them are useless at playing snake.  The following allows you to play using ollama and gemma2 9b.

Mistral Large is actually pretty decent at playing Minesweeper

```bash
python main_simple.py play --env snake --agent snake_gpt4o --provider ollama --model mistral-large
```