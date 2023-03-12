from typing import List, Optional

from snake import Action, BaseAgent, CellState, main, BOARD_SIZE

from collections import deque

#################################################################
#   Modify the Agent class below to implement your own agent.   #
#   You may define additional methods as you see fit.           #
#################################################################

Position = tuple[int, int]


class Agent(BaseAgent):
    """An agent for the snake competition on DOXA."""

    def __init__(self) -> None:
        super().__init__()
        self.dist_to_source = None
        self.edge_to = None
        self.reset()

    def reset(self) -> None:
        self.dist_to_source = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.edge_to = [[(-1, -1) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    @staticmethod
    def __pos(board: List[List[CellState]], cell_state: CellState) -> Position:
        for i, row in enumerate(board):
            for j, state in enumerate(row):
                if state == cell_state:
                    return i, j

    @staticmethod
    def __diff(a: Position, b: Position) -> Position:
        return (a[0] - b[0]) % BOARD_SIZE, (a[1] - b[1]) % BOARD_SIZE

    def bfs(self, board: List[List[CellState]], source: Position) -> None:
        queue = deque()
        queue.append(source)

        while len(queue) != 0:
            vertex = queue.popleft()

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                row = (vertex[0] + dr) % BOARD_SIZE
                col = (vertex[1] + dc) % BOARD_SIZE

                if board[row][col] == CellState.TAIL:
                    continue

                if self.dist_to_source[row][col] == -1:
                    queue.append((row, col))
                    self.dist_to_source[row][col] = self.dist_to_source[vertex[0]][vertex[1]] + 1
                    self.edge_to[row][col] = vertex

    def shortest_path_to(self, vertex: Position, source: Position) -> Optional[Position]:
        if self.dist_to_source[vertex[0]][vertex[1]] == -1:
            return None

        path = []
        curr = vertex

        while curr != source:
            path.append(curr)
            curr = self.edge_to[curr[0]][curr[1]]

        return path[-1]

    @staticmethod
    def act(step: Position) -> Action:
        if step[0] == 1:
            return Action.DOWN
        elif step[0] == 9:
            return Action.UP
        elif step[1] == 1:
            return Action.RIGHT
        else:
            return Action.LEFT

    async def make_move(self, board: List[List[CellState]]) -> Action:
        """Makes a move.
        Args:
            board (List[List[CellState]]): The current state of the board.
        Returns:
            Action: The direction to move in.
        """
        head = Agent.__pos(board, CellState.HEAD)
        fruit = Agent.__pos(board, CellState.FRUIT)

        self.bfs(board, head)
        cell = self.shortest_path_to(fruit, head)

        step = Agent.__diff(cell, head)
        self.reset()

        return self.act(step)


if __name__ == "__main__":
    main(Agent())
