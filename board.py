from enum import Enum
import random

from dijkstra import board_to_tuple


class Direction(Enum):
    UP = (-1, 0)  # 'up'  (-1, 0)
    DOWN = (1, 0)  # 'down'  (1, 0)
    LEFT = (0, -1)  # 'left'  (0, -1)
    RIGHT = (0, 1)  # 'right'  (0, 1)


class Board:
    def __init__(self):
        self.board = [[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 0]]
        self.empty = [2, 2]
        self.shuffle(100)

    def flatten(self):
        return tuple([*self.board[0], *self.board[1], *self.board[2]])

    def get_number(self, row, col):
        return self.board[row][col]

    def move(self, direction: Direction) -> bool:
        x, y = self.empty
        if direction == Direction.DOWN and x > 0:
            self.board[x][y], self.board[x-1][y] = self.board[x-1][y], self.board[x][y]
            self.empty = [x-1, y]
            return True
        elif direction == Direction.UP and x < 2:
            self.board[x][y], self.board[x+1][y] = self.board[x+1][y], self.board[x][y]
            self.empty = [x+1, y]
            return True
        elif direction == Direction.RIGHT and y > 0:
            self.board[x][y], self.board[x][y-1] = self.board[x][y-1], self.board[x][y]
            self.empty = [x, y-1]
            return True
        elif direction == Direction.LEFT and y < 2:
            self.board[x][y], self.board[x][y+1] = self.board[x][y+1], self.board[x][y]
            self.empty = [x, y+1]
            return True
        return False

    def is_solved(self) -> bool:
        correct_board = [[1, 2, 3],
                         [4, 5, 6],
                         [7, 8, 0]]
        return self.board == correct_board

    def tuple(self):
        return board_to_tuple(self.board)

    def shuffle(self, i=100):
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        n = 0
        while n < i:
            direction = random.choice(directions)
            ret = self.move(direction)
            n += int(ret)

