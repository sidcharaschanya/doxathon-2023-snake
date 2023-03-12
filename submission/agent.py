import math
from typing import List, Optional

from snake import Action, BaseAgent, CellState, main, BOARD_SIZE

from collections import deque


#################################################################
#   Modify the Agent class below to implement your own agent.   #
#   You may define additional methods as you see fit.           #
#################################################################


class Agent(BaseAgent):
    """An agent for the snake competition on DOXA."""

    def __init__(self):
        super().__init__()
        self.dist_to_source = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.edge_to = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    @staticmethod
    def __norm(pos: tuple[int, int]):
        return math.sqrt(pos[0] ** 2 + pos[1] ** 2)

    def bfs(self, board: List[List[CellState]], source: tuple[int, int]):
        queue = deque()
        queue.append(source)

        while len(queue) != 0:
            vertex = queue.popleft()

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                row, col = vertex[0] + dr, vertex[1] + dc

                if row < 0 or col < 0 or row > BOARD_SIZE - 1 or col > BOARD_SIZE - 1:
                    continue

                if board[row][col] == CellState.TAIL:
                    continue

                if self.dist_to_source[row][col] == -1:
                    queue.append((row, col))
                    self.dist_to_source[row][col] = self.dist_to_source[vertex[0]][vertex[1]] + 1
                    self.edge_to[row][col] = vertex

    def shortest_path_to(self, vertex, source) -> Optional[tuple[int, int]]:
        if not self.dist_to_source[vertex[0]][vertex[1]] != -1:
            return None
        path = []
        curr = vertex
        while curr != source:
            path.append(curr)
            curr = self.edge_to[curr[0]][curr[1]]
        return path[-1]

    async def make_move(self, board: List[List[CellState]]) -> Action:
        """Makes a move.
        Args:
            board (List[List[CellState]]): The current state of the board.
        Returns:
            Action: The direction to move in.
        """
        head, fruit = None, None

        for i, row in enumerate(board):
            for j, cell_state in enumerate(row):
                if cell_state == CellState.HEAD:
                    head = (i, j)

                if cell_state == CellState.FRUIT:
                    fruit = (i, j)

        self.bfs(board, head)
        cell = self.shortest_path_to(fruit, head)

        move = (cell[0] - head[0], cell[1] - head[1])

        if Agent.__norm((fruit[0] - head[0], fruit[1] - head[1])) == 1:
            self.dist_to_source = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
            self.edge_to = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        if move[0] == 1:
            return Action.DOWN
        elif move[0] == -1:
            return Action.UP
        elif move[1] == 1:
            return Action.RIGHT
        else:
            return Action.LEFT


if __name__ == "__main__":
    main(Agent())
