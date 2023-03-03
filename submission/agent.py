import random
from typing import List, Tuple

from snake import BaseAgent, RemoteSnakeGame

#################################################################
#   Modify the Agent class below to implement your own agent.   #
#   You may define additional methods as you see fit.           #
#################################################################


class Agent(BaseAgent):
    """An agent for the snake competition on DOXA."""

    def make_move(self, board: List[List[str]]) -> Tuple[Tuple[int, int], str]:
        """Makes a move.
        Args:
            board (List[List[str]]): The current state of the board.
        Returns:
            Tuple[Tuple[int, int], str]: The coordinates of the head and direction of the snake.
        """

        # Find all the free tiles across all playable boards
        possible_moves = ["N", "E", "S", "W"]

        # Pick a valid move uniformly at random
        return (self.coords[-1], random.choice(possible_moves))


def main():
    # Instantiate the agent
    agent = Agent()

    # Start playing the game remotely
    RemoteSnakeGame(agent).play()

    # Start playing the game on DOXA
    # SnakeGame(agent).play()


if __name__ == "__main__":
    main()
