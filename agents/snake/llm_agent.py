# File: agents/snake/llm_agent.py
import time
from agents.provider_type import ProviderType
from agents.base_llm_agent import BaseLLMAgent
from agents.snake.agent_action import AgentAction
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class LLMAgent(BaseLLMAgent):
    def __init__(self, id: str, name: str, description: str, provider: ProviderType, model_name: str):
        prompt_template = """
        You are an AI controlling a snake in a classic Snake game. The game is played on a rectangular grid.

Grid Information:

- Size: 10 x 10
- Grid System: [x, y]
- Zero-based coordinate system
- Top-left coordinate: [0, 0]
- Bottom-right coordinate: [9, 9]
- Coordinates format: [column_number, row_number] (zero-based, x, y format where x is the column and y is the row)
- Moving UP decreases Y by 1.
- Moving DOWN increases Y by 1.
- Moving LEFT decreases X by 1.
- Moving RIGHT increases X by 1.

Grid symbols:

- H : Head of the snake (current position)
- O : Body of the snake
- F : Food that the snake should eat
- . : Empty square

Current game state:
{state}

Snake game strategy:
1. Primary goal: Move towards the food (F) to grow the snake.
2. Avoid collisions: Don't move into walls or the snake's body (O).
3. Plan ahead: Consider the snake's length when moving towards food.
4. Use space efficiently: Try to move in a way that leaves open paths.
5. In tight spaces, follow the snake's tail to survive.
6. If no clear path to food exists, move to maximize empty space around the head.

Based on the current state and strategy, decide the snake's next move.
Choose from: UP, DOWN, LEFT, RIGHT

Consider these factors in order:
1. Immediate survival (avoid collisions)
2. Moving towards food (F) to grow the snake and achieve a high score.
3. Long-term survival (maintaining open paths)

Provide your answer as a single word (UP, DOWN, LEFT, or RIGHT) with no additional explanation.
        """
            
        # call the parent
        super().__init__(id, name, description, provider, model_name, prompt_template)

        # update the prompt template to CoT version
        self.prompt_template = prompt_template

        # set the prompt template
        self.prompt = PromptTemplate(input_variables=["state","size","visited"], template=prompt_template)
        
        # setup the chain with the prompt and llm
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def get_action(self, step:int, state: str):
        # call the llm
        response = self.chain.run(state=state)

        # extract the thought process and final output
        thought_process = self.extract_tag_content(response, "agentThinking")
        final_output = self.extract_tag_content(response, "finalOutput")
        time_completed = time.strftime('%Y-%m-%d %H:%M:%S')

        # log the state, thought process, and decision
        self.logger.log_decision(self.game_id, step, state, thought_process, final_output, response, time_completed)

        # map the action
        action_map = {
            "UP": AgentAction.UP,
            "DOWN": AgentAction.DOWN,
            "LEFT": AgentAction.LEFT,
            "RIGHT": AgentAction.RIGHT
        }

        # return the action
        return action_map.get(final_output.strip().upper(), AgentAction.RIGHT)